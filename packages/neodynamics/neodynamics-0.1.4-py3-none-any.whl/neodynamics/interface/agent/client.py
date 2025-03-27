import msgpack
import grpc
import requests

from gymnasium import Env, spaces
from gymnasium.core import ActType, ObsType

# Add the interface directory to the path to import the generated gRPC code
from neodynamics.interface import Empty, ObservationRequest, AgentServiceStub
from neodynamics.interface.utils import native_to_numpy, numpy_to_native, native_to_numpy_space

class AgentClient(Env):
    """
    A Gym environment that connects to a remote environment via gRPC.

    This class implements the Gym interface and forwards all calls to a remote
    environment server running the AnyLogic Stock Management environment.

    Args:
        server_address (str): The address of the gRPC server (e.g., "localhost:50051")
        render_mode (str, optional): The render mode to use. Defaults to None.
        init_args (dict, optional): Additional arguments to pass to the environment initialization.
    """

    def __init__(self, server_address: str):
        # Connect to the gRPC server
        self.channel = grpc.insecure_channel(server_address)
        self.stub = AgentServiceStub(self.channel)

        # Initialize the remote environment
        init_request = Empty()

        # Call the Init method and get space information
        spaces_response = self.stub.GetSpaces(init_request)

        # Set up observation space
        space_dict = {}
        for name, proto_space in spaces_response.observation_space.items():
            space_dict[name] = native_to_numpy_space(proto_space)
        self.observation_space = spaces.Dict(space_dict)

        # Set up action space
        self.action_space = native_to_numpy_space(spaces_response.action_space)

    def get_action(self, observation: ObsType) -> ActType:
        """Get an action from the agent."""
        # Convert numpy arrays to lists for serialization
        serializable_observation = {}
        for key, value in observation.items():
            serializable_observation[key] = numpy_to_native(value, self.observation_space[key])
        observation_request = ObservationRequest(observation=msgpack.packb(serializable_observation, use_bin_type=True))

        # Call the GetAction method
        action_response = self.stub.GetAction(observation_request)

        # Deserialize the action
        action = msgpack.unpackb(action_response.action, raw=False)
        numpy_action = native_to_numpy(action, self.action_space)

        return numpy_action

class DeployedAgentClient(AgentClient):
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key
        self.headers = None
        if api_key is not None:
            self.headers = {
                'Content-Type': 'application/json',
                'X-Neo-API-Key': self.api_key
            }

    def get_action(self, obs):
        obs_dict = {k: v.tolist() for k, v in obs.items()}
        response = requests.post(self.url, json={"observation": obs_dict}, headers=self.headers)
        return response.json().get("action")


def main(server_address: str = "localhost:50051", num_steps: int = 5):
    """
    Run a simple test of the EnvironmentClient.

    Args:
        server_address: The address of the server (e.g., "localhost:50051")
        num_steps: Number of steps to run in the test
    """
    try:
        # Create a remote agent
        agent = AgentClient(server_address)

        # Run a few steps
        for i in range(num_steps):
            obs = agent.observation_space.sample()
            action = agent.get_action(obs)
            assert agent.action_space.contains(action), f"Action {action} not in action space {agent.action_space}"

            print(f"Observation: {obs}")
            print(f"Action: {action}")

        # Print success message if no errors occurred
        print("\nSuccess! The agent client is working correctly.")

    except Exception as e:
        print(f"\nError: {e}")
        print("Failed to connect to or interact with the agent server.")
        raise


# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the AgentClient")
    parser.add_argument("--address", default="localhost:50051",
                        help="AServer address (default: localhost:50051)")
    parser.add_argument("--steps", type=int, default=5,
                        help="Number of steps to run in the test (default: 5)")

    args = parser.parse_args()

    try:
        main(args.address, args.steps)
    except Exception:
        import sys
        sys.exit(1)