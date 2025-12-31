

from ml.inference.skill_extractor import SkillExtractor
from ml.inference.salary_predictor import SalaryPredictor
from ml.inference.forecaster import SkillForecaster

class ModelManager:
    def __init__(self):
        self.skill_extractor = SkillExtractor()
        self.salary_predictor = SalaryPredictor()
        self.forecaster = SkillForecaster()
        self._models_loaded = False
    
    async def load_models(self):
        try:
            await self.skill_extractor.load_model()
            await self.salary_predictor.load_model()
            await self.forecaster.load_models()
            self._models_loaded = True
        except Exception as e:
            print(f"Warning: Some models failed to load: {e}")
            self._models_loaded = False
    
    def models_ready(self) -> bool:
        return self._models_loaded