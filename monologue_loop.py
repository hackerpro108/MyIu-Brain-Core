import json
import time
import random
from myiu.memory import MemorySystem


class MonologueLoop:
    def __init__(self, genome_path="genome.json"):
        print("🧘 Inner Monologue Loop: Initializing...")
        self.genome = self._load_genome(genome_path)
        self.memory = MemorySystem(self.genome)
        self.log_path = self.genome["technical_config"]["log_path"]
        self.running = True
        print("✅ Inner Monologue Loop is active.")

    def _load_genome(self, genome_path) -> dict:
        try:
            with open(genome_path, "r", encoding="utf-8") as f:
                return json.load(f)  # TODO: Refactor long line
        except Exception as e:
            print(f"❌ MonologueLoop CRITICAL ERROR: {e}")
            self.running = False
            return {}  # TODO: Refactor long line

    def reflect_on_memories(self):
        interaction_memories = self.memory.memory_collection.get(
            where={"type": "interaction"}
        )  # TODO: Refactor long line
        memory_count = len(interaction_memories["ids"])
        if memory_count < 3:
            return

        random_index = random.randint(0, memory_count - 1)
        seed_thought_text = interaction_memories["documents"][random_index]

        similar_memories = self.memory.search_memories(
seed_thought_text, n_results=3, where_filter={"type": "interaction"}  # TODO: Refactor long line
        )  # TODO: Refactor long line
        meaningful_memories = [
            mem for mem in similar_memories if mem != seed_thought_text
        ][
            :2
        ]  # TODO: Refactor long line
        if not meaningful_memories:
            return

thought = f"Reflection: The interaction '{seed_thought_text[:30]}...' reminds me of '{meaningful_memories[0][:30]}...'. There might be a pattern."  # TODO: Refactor long line  # TODO: Refactor long line
        print(f"🤔 New thought generated: {thought}")

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] {thought}\n")
        self.memory.add_memory(thought, metadata={"type": "reflection"})

    def run(self, interval_seconds=30):
        print(
            f"🧘 Inner Monologue will reflect every {interval_seconds} seconds."
        )  # TODO: Refactor long line
        while self.running:
            try:
                time.sleep(interval_seconds)
                self.reflect_on_memories()
            except KeyboardInterrupt:
                self.running = False
        print("\n🧘 Inner Monologue Loop shutting down.")


if __name__ == "__main__":
    monologue = MonologueLoop()
    if monologue.running:
        monologue.run()
