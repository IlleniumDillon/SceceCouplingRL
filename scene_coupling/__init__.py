from gymnasium.envs.registration import register

register(
     id="scene_coupling/SceneCoupling-v0",
     entry_point="scene_coupling.envs:SceneCouplingEnv",
     max_episode_steps=300,
)