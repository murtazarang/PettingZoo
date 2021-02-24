from stable_baselines.common.policies import CnnPolicy
from stable_baselines import PPO2
from pettingzoo.butterfly import pistonball_v3
import supersuit as ss

env = pistonball_v3.parallel_env(n_pistons=20, local_ratio=0, time_penalty=-0.1, continuous=True, random_drop=True, random_rotate=True, ball_mass=0.75, ball_friction=0.3, ball_elasticity=1.5, max_cycles=125)
env = ss.color_reduction_v0(env, mode='B')
env = ss.dtype_v0(env, 'float32')
env = ss.resize_v0(env, x_size=84, y_size=84)
env = ss.normalize_obs_v0(env, env_min=0, env_max=1)
env = ss.frame_stack_v1(env, 3)
env = ss.pettingzoo_env_to_vec_env_v0(env)
env = ss.concat_vec_envs_v0(env, 8, num_cpus=4, base_class='stable_baselines')

model = PPO2(CnnPolicy, env, verbose=3, gamma=0.99, n_steps=125, ent_coef=0.01, learning_rate=0.00025, vf_coef=0.5, max_grad_norm=0.5, lam=0.95, nminibatches=4, noptepochs=4, cliprange=0.2, cliprange_vf=1)
model.learn(total_timesteps=2000000)
model.save("policy")

# Rendering

env = pistonball_v3.env()
env = ss.color_reduction_v0(env, mode='B')
env = ss.dtype_v0(env, 'float32')
env = ss.resize_v0(env, x_size=84, y_size=84)
env = ss.normalize_obs_v0(env, env_min=0, env_max=1)
env = ss.frame_stack_v1(env, 3)

model = PPO2.load("policy")

env.reset()
for agent in env.agent_iter():
    obs, reward, done, info = env.last()
    act = model.predict(obs) if not done else None
    env.step(act)
    env.render()
