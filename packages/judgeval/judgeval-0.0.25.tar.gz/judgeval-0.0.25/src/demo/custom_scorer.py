from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import JudgevalScorer, AnswerRelevancyScorer

client = JudgmentClient()


class SampleScorer(JudgevalScorer):

    def __init__(
        self,
        threshold=0.5,
        score_type="Sample Scorer",
        include_reason=True,
        async_mode=True,
        strict_mode=False,
        verbose_mode=True
    ):
        super().__init__(score_type=score_type, threshold=threshold)
        self.threshold = 1 if strict_mode else threshold
        # Optional attributes
        self.include_reason = include_reason
        self.async_mode = async_mode
        self.strict_mode = strict_mode
        self.verbose_mode = verbose_mode

    def score_example(self, example):
        self.score = 1.0
        self.success = True
        return self.score
    
    async def a_score_example(self, example):
        print("Scoring example...")
        self.score = 1.0
        self.success = True
        return self.score
    
    def _success_check(self):
        print("Checking success...")
        if self.error is not None:
            return False
        return self.score >= self.threshold
    
    # @property
    # def __name__(self):
    #     return "Sample Scorer"
    

if __name__ == "__main__":
    scorer = SampleScorer()
    example = Example(
        input="What is the capital of France?",
        actual_output="Paris",
    )
    results = client.run_evaluation(examples=[example], 
                                    scorers=[scorer], 
                                    model="gpt-4o", 
                                    project_name="custom-scorer", 
                                    eval_run_name="custom-scorer-demo-10",
                                    ignore_errors=True)
