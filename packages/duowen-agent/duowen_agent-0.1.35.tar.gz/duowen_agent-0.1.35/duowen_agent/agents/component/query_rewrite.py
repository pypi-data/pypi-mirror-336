from typing import Literal, Optional, List

from pydantic import BaseModel, Field

from duowen_agent.agents.component.base import BaseComponent
from duowen_agent.llm import OpenAIChat
from duowen_agent.prompt.prompt_build import (
    GeneralPromptBuilder,
    practice_dir,
    prompt_now_day,
)
from duowen_agent.utils.core_utils import json_observation
from duowen_agent.utils.string_template import StringTemplate


class QuestionCategories(BaseModel):
    conflict: Optional[str] = Field(
        default=None, description="当存在跨级特征时的矛盾点"
    )
    reason: str = Field(..., description="16字内核心依据")
    category_name: Literal["简单直接", "多步骤", "多主题"] = Field(
        description="Exactly the name of the category that matches"
    )


class QueryClassification(BaseComponent):

    def __init__(self, llm_instance: OpenAIChat, **kwargs):
        self.llm_instance = llm_instance
        self.kwargs = kwargs

    @staticmethod
    def build_prompt():
        GeneralPromptBuilder(
            instruction="""根据问题特征进行三层稳定性分类，采用正交判别法

# 核心规则（独立互斥）
1. **简单直接类**必须满足：
   - 执行路径唯一且标准化（查表/转换/计算）
   - 所需参数≤2个且无动态依赖（如天气无需实时数据）

2. **多步骤类**触发条件：
   - 存在显性逻辑链 (因果/比较/条件) 
   OR
   - 需要3+参数动态组合（如温度+风速+场合）

3. **多主题类**严格标准：
   - 涉及两个独立知识域（领域重叠度＜30%）
   - 需要调用不同框架进行解答""",
            step="""```mermaid
graph TD
    A[原始问题] --> B{包含'>1'个问号}
    B -->|是| C[领域离散检测]
    C -->|离散度>0.6| D[多主题]
    B -->|否| E{存在逻辑关键词}
    E -->|是| F[多步骤]
    E -->|否| G[参数复杂度分析]
    G -->|参数≥3| F
    G -->|参数<3| H[简单直接]
```""",
            output_format=QuestionCategories,
            sample="""
输入：孙悟空和钢铁侠谁更加厉害？
输出：
```json
{"conflict":"表面简单但涉及跨体系能力比较","reason":"跨作品战力需多维评估","category_name":"多步骤"}
```

输入：如何用python编写排序算法？
输出：
```json
{"reason":"标准算法单文档可覆盖","category_name":"简单直接"}
```
""",
            note="""- 置信度锚定：各分类初始置信度 ≠ 可重叠范围
- 最终决策树：任一节点判定后立即阻断下游判断
- 语义消毒：自动滤除修饰性副词与情感词汇""",
        ).export_yaml(practice_dir + "/query_classification.yaml")

    def run(
        self,
        question: str,
        **kwargs,
    ) -> QuestionCategories:
        _prompt = GeneralPromptBuilder.load("query_classification").get_instruction(
            question
        )

        _res = self.llm_instance.chat(_prompt)

        _res: QuestionCategories = json_observation(_res, QuestionCategories)

        return _res


class SubTopic(BaseModel):
    original_subtopic: str = Field(..., description="原始问题中识别出的子主题描述")
    rewritten_query: str = Field(..., description="改进后的具体查询语句")


class TopicCategories(BaseModel):
    splitting: List[SubTopic] = Field(
        ..., description="必须生成**2-5个**改写版本，每个查询语句不超过25个汉字"
    )


class TopicSpliter(BaseComponent):
    def __init__(self, llm_instance: OpenAIChat, **kwargs):
        self.llm_instance = llm_instance
        self.kwargs = kwargs

    @staticmethod
    def build_prompt():
        GeneralPromptBuilder(
            instruction="当用户输入的问题包含多个隐藏的子问题或涉及不同领域时，将其分解为独立的具体查询并生成改写版本。为每个子主题生成聚焦单一意图的查询，确保全面覆盖原始问题的各个维度。",
            step="""1. **识别隐藏子问题**：先分析用户问题的语义结构，识别出隐含的独立话题或追问方向
2. **语义解耦**：将这些复合话题拆解为2-5个彼此独立的核心查询要素
3. **针对性改写**：针对每个单点问题生成优化后的查询版本，要求：
   - 保持原问题关键信息
   - 使用领域相关术语
   - 包含明确的范围限定词""",
            output_format=TopicCategories,
            sample="""
输入："我应该去哪里学习AI又适合旅游？"
输出：
```json
{
    "splitting": [
        {
            "original_subtopic": "教育质量",
            "rewritten_query": "全球人工智能专业顶尖高校排名",
        },
        {
            "original_subtopic": "生活体验",
            "rewritten_query": "留学热门城市旅游景点推荐",
        },
    ]
}
```""",
            note="""- 当问题存在多维度交叉时（如"[海外购房与税务]"），需分别生成"海外购房流程指南"和"跨境资产税务申报规则"两个独立查询
- 智能处理模糊表达：对于"好的科技公司标准"应拆解为"科技公司估值模型"和"员工福利标杆企业案例"
- 禁用通用型查询：将"有什么新技术？"强化为"[年度突破性半导体技术创新]"
- 确保可独立检索性：每个改写后的查询应能在主流搜索引擎中获得直接答案""",
        ).export_yaml(practice_dir + "/topic_spliter.yaml")

    def run(
        self,
        question: str,
        **kwargs,
    ) -> TopicCategories:
        _prompt = GeneralPromptBuilder.load("topic_spliter").get_instruction(question)

        _res = self.llm_instance.chat(_prompt)

        _res: TopicCategories = json_observation(_res, TopicCategories)

        return _res


class AnalyzedIntents(BaseModel):
    surface: str = Field(..., description="表层需求")
    practical: str = Field(..., description="实用需求")
    emotional: str = Field(..., description="情感驱动")
    social: str = Field(..., description="社交关联")
    identity: str = Field(..., description="身份投射")
    taboo: str = Field(..., description="禁忌边界")
    shadow: str = Field(..., description="影子动机")


class OptimizedQueries(BaseModel):
    ExpertSkeptic: str = Field(..., description="质疑型查询")
    DetailAnalyst: str = Field(..., description="数据型查询")
    HistoricalResearcher: str = Field(..., description="历时性查询")
    ComparativeThinker: str = Field(..., description="对比式查询")
    TemporalContext: str = Field(..., description="带时间戳的查询")
    Globalizer: str = Field(..., description="多语言权威查询")
    RealitySkeptic: str = Field(..., description="反向论证查询")


class MultiSearch(BaseModel):
    analyzed_intents: AnalyzedIntents = Field(..., description="七层意图分析")
    optimized_queries: OptimizedQueries = Field(..., description="认知视角扩展")


class QueryExtend(BaseComponent):
    def __init__(self, llm_instance: OpenAIChat, **kwargs):
        self.llm_instance = llm_instance
        self.kwargs = kwargs

    @staticmethod
    def build_prompt():
        GeneralPromptBuilder(
            instruction="""通过七层心理模型深度解析用户潜在需求，生成多维高价值搜索查询变体

**核心能力**
1. 执行七层级需求穿透分析（表层意图→影子意图）
2. 按七种认知维度自动生成结构化查询组合""",
            step="""### 第一步：七层意图分析
对输入查询进行逐层深度解构：

1. **表层需求** → 字面诉求的显性表达
2. **实用需求** → 待解决的具体问题/目标
3. **情感驱动** → 恐惧/渴望/焦虑等核心情绪
4. **社交关联** → 人际关系/社会地位关联性
5. **身份投射** → 目标身份构建/身份回避
6. **禁忌边界** → 不可明言的隐藏议题
7. **影子动机** → 连用户都未察觉的无意识需求

### 第二步：认知视角扩展
为每种专家角色生成严格匹配其特征的查询：

1. **质疑专家** → 专门寻找[反例/失败案例/理论漏洞]
2. **数据专员** → 要求[精确数值/技术参数/方法论细节]
3. **历史学者** → 追溯[发展历程/古早版本/演进图谱]
4. **对比大师** → 建立[多维度PK矩阵/优劣势天平表]
5. **时效猎手** → 融合[当前年月日]进行新鲜度验证
6. **语言属地专家** → 根据主题选定[德语/日语/意大利语]等原生权威语言
7. **证伪狂人** → 构建[反向论证链/矛盾证据集合]""",
            output_format=MultiSearch,
            #             sample=StringTemplate(
            #                 """
            # 输入: 宝马二手车价格
            #
            # 输出:
            # ```json
            # {
            #   "analyzed_intents": {
            #     "surface": "查询宝马二手车市场价格信息",
            #     "practical": "评估目标车型市场价值或出售车辆定价依据",
            #     "emotional": "焦虑（担心交易不公）与渴望（追求物有所值）",
            #     "social": "维护社会形象避免被视作交易新手",
            #     "identity": "通过宝马品牌二手车构建成功人士身份认同",
            #     "taboo": "经济调整期家庭财务压力（语义置换处理）",
            #     "shadow": "达克效应导致的车况高估与确认偏误驱动的价格锚定"
            #   },
            #   "optimized_queries": {
            #     "ExpertSkeptic": "宝马二手车价格虚高的案例及第三方检测报告",
            #     "DetailAnalyst": "宝马3系2018款2.0T二手车残值率与维修成本参数表",
            #     "HistoricalResearcher": "宝马5系E60代二手车2010-2024年价格波动周期分析",
            #     "ComparativeThinker": "宝马3系/5系/X3同配置二手车2024年价格对比（含里程/保养/事故史维度）",
            #     "TemporalContext": "截止今天{{current data}},宝马525i二手车在德国市场的最新报价与保值率",
            #     "Globalizer": "BMW Gebrauchtwagen Probleme",  // 宝马是德国车，德国人对这车的了解肯定最深，德国车主的真实评价会更有参考价值。
            #     "RealitySkeptic": "反驳宝马二手车价格高于新车的逻辑漏洞及2023年市场数据验证"
            #   }
            # }
            # ```
            # """,
            #                 template_format="jinja2",
            #             ),
            note=StringTemplate(
                """## 执行标准

1. 影子动机分析必须运用认知偏误理论（如达克效应、确认偏误）
2. 多语言查询必须符合行业权威语言的ISO 639-1标准代码
3. 时间戳格式强制采用RFC 3339标准（示例：2024-03-15T08:00:00Z）
4. 对比类查询必须包含≥3个可比项及量化对比维度

## 关键注意

- 禁忌分析层必须通过语义置换技术处理敏感词（如用"经济调整"代替"裁员"）
- 情感驱动识别需匹配普拉切克情感轮盘中的8种基本情绪
- 权威语言选择须参照MIT全球化研究智库的行业语言地图数据
- {{prompt_now_day}} """,
                template_format="jinja2",
            ),
        ).export_yaml(practice_dir + "/query_extend.yaml")

    def run(
        self,
        question: str,
        **kwargs,
    ) -> MultiSearch:
        _prompt = GeneralPromptBuilder.load("query_extend").get_instruction(
            question, temp_vars={"prompt_now_day": prompt_now_day()}
        )

        # print(_prompt.get_format_messages())

        _res = self.llm_instance.chat(_prompt)
        # print(_res)
        _res: MultiSearch = json_observation(_res, MultiSearch)

        return _res


if __name__ == "__main__":
    QueryClassification.build_prompt()
    TopicSpliter.build_prompt()
    QueryExtend.build_prompt()
