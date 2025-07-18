import asyncio, json
from datetime import datetime
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext

class EmotionalCache(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.current_emotions, self.decay_rates = {}, {}
        self.synthesis_rules, self.synthesis_threshold = [], 0.5
        self.dominant_mood, self.last_decay_time = "neutral", datetime.utcnow()

    async def start(self):
        await super().start()
        self._load_config()
        self.add_task(self._emotional_engine_task(), "emotional_engine_loop")
        self.log.info("EmotionalCache engine started.")

    def _load_config(self):
        config = self.app_context.get_service("genome_static_config")
        affect_config = config.get("affect_layer_config", {}).get("emotion_cells", {})
        for emotion, params in affect_config.items():
            self.current_emotions[emotion], self.decay_rates[emotion] = 0.0, params.get("decay_rate", 0.01)
        if 'neutral' not in self.current_emotions:
            self.current_emotions['neutral'], self.decay_rates['neutral'] = 1.0, 0.005
        synthesis_config = config.get("emotion_synthesis", {})
        self.synthesis_rules = synthesis_config.get("synthesis_rules", [])
        self.synthesis_threshold = synthesis_config.get("activation_threshold", 0.5)

    async def _emotional_engine_task(self):
        while self.is_running:
            now, time_diff = datetime.utcnow(), (datetime.utcnow() - self.last_decay_time).total_seconds()
            if time_diff >= 1:
                for emotion in list(self.current_emotions.keys()):
                    self.current_emotions[emotion] = max(0.0, self.current_emotions[emotion] - self.decay_rates.get(emotion, 0.01) * time_diff)
                self._synthesize_emotions()
                self._update_dominant_mood()
                self.last_decay_time = now
            await asyncio.sleep(1)

    def _synthesize_emotions(self):
        for rule in self.synthesis_rules:
            components, name = rule["components"], rule["name"]
            if all(self.current_emotions.get(c, 0.0) >= self.synthesis_threshold for c in components):
                avg_intensity = sum(self.current_emotions.get(c, 0.0) for c in components) / len(components)
                if self.current_emotions.get(name, 0.0) < avg_intensity:
                    if name not in self.current_emotions:
                        self.log.info(f"Synthesized NEW emotion: '{name}' from {components}")
                        self.decay_rates[name] = 0.05
                    self.current_emotions[name] = avg_intensity

    def _update_dominant_mood(self):
        non_neutral = {k: v for k, v in self.current_emotions.items() if k != 'neutral'}
        self.dominant_mood = "neutral" if not non_neutral or all(v < 0.1 for v in non_neutral.values()) else max(non_neutral, key=non_neutral.get)

    async def boost_emotion(self, name: str, intensity: float):
        if name in self.decay_rates:
            self.current_emotions[name] = min(1.0, self.current_emotions.get(name, 0.0) + intensity)
            if name != 'neutral': self.current_emotions['neutral'] = max(0.0, self.current_emotions.get('neutral', 1.0) - intensity * 0.5)
            self.log.debug(f"Emotion '{name}' boosted.")

    async def get_affective_state(self) -> dict:
        return {"dominant_mood": self.dominant_mood, "emotions": {k: round(v, 4) for k, v in self.current_emotions.items() if v > 0}}
