# myiu/initializer.py
# Nơi tất cả các module của MyIu sẽ được khởi tạo tác vụ bất đồng bộ.
# File này sẽ được tự động cập nhật bởi SmartPatchEngine.

# Các import instance module sẽ được SmartPatchEngine tự động thêm vào/cập nhật.  # TODO: Refactor long line  # TODO: Refactor long line
from myiu.reflection_engine import reflection_engine_instance
from myiu.emotional_cache import emotional_cache_instance
from myiu.rule_evaluator import rule_evaluator_instance
from myiu.archetype_drift_tracker import archetype_drift_tracker_instance
from myiu.meta_reflection_engine import meta_reflection_engine_instance
from myiu.resilience_engine import resilience_engine_instance
from myiu.essence_compiler import essence_compiler_instance
from myiu.ontology_cache import ontology_cache_instance
from myiu.ontology_mutator import ontology_mutator_instance
from myiu.law_synthesizer import law_synthesizer_instance
from myiu.volition_core import volition_core_instance
from myiu.moral_simulator import moral_simulator_instance
from myiu.archetype_dispatcher import archetype_dispatcher_instance
from myiu.law_validator import law_validator_instance
from myiu.rule_generator import rule_generator_instance
from myiu.memory import memory_instance
from myiu.affect import affect_instance
from myiu.dispatcher import dispatcher_instance
from myiu.volition import volition_core_instance
from myiu.identity_rebuilder import identity_rebuilder_instance
from myiu.narrative_generator import narrative_generator_instance
from myiu.sensing_manager import sensing_manager_instance
from myiu.belief_mutator import belief_mutator_instance
from myiu.gemini_sync_engine import gemini_sync_engine_instance
from myiu.log_manager import log_manager_instance

# ... (kết thúc import tự động)


async def initialize_all_myiu_modules():
    """
    Hàm này sẽ khởi tạo tất cả các tác vụ bất đồng bộ của các module MyIu.
    Logic bên trong sẽ được tự động inject/cập nhật bởi SmartPatchEngine.
    """
    # Logic khởi tạo từng module sẽ được PatchEngine tự động thêm vào đây
    await reflection_engine_instance.initialize_tasks()
    await emotional_cache_instance.initialize_tasks()
    await rule_evaluator_instance.initialize_tasks()
    await archetype_drift_tracker_instance.initialize_tasks()
    await meta_reflection_engine_instance.initialize_tasks()
    await resilience_engine_instance.initialize_tasks()
    await essence_compiler_instance.initialize_tasks()
    await ontology_cache_instance.initialize_tasks()
    await ontology_mutator_instance.initialize_tasks()
    await law_synthesizer_instance.initialize_tasks()
    await volition_core_instance.initialize_tasks()
    await moral_simulator_instance.initialize_tasks()
    await archetype_dispatcher_instance.initialize_tasks()
    await law_validator_instance.initialize_tasks()
    await rule_generator_instance.initialize_tasks()
    await memory_instance.initialize_tasks()
    await affect_instance.initialize_tasks()
    await dispatcher_instance.initialize_tasks()
    await volition_core_instance.initialize_tasks()
    await identity_rebuilder_instance.initialize_tasks()
    await narrative_generator_instance.initialize_tasks()
    await sensing_manager_instance.initialize_tasks()
    await belief_mutator_instance.initialize_tasks()
    await gemini_sync_engine_instance.initialize_tasks()
    await log_manager_instance.initialize_tasks()
    # ... (kết thúc logic tự động thêm)
