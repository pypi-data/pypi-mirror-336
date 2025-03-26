import numpy as np
from gymnasium import spaces

def numpy_to_native_space(space, space_proto):
    """Helper method to set space information based on space type."""
    if isinstance(space, spaces.Box):
        space_proto.space_type = "Box"
        space_proto.low.extend(space.low.flatten().tolist())
        space_proto.high.extend(space.high.flatten().tolist())
        space_proto.shape.extend(space.shape)
        space_proto.dtype = str(space.dtype)
    elif isinstance(space, spaces.Discrete):
        space_proto.space_type = "Discrete"
        space_proto.n = space.n.item()
        space_proto.shape.extend([1])  # Discrete spaces have shape (1,)
        space_proto.dtype = str(space.dtype)
    elif isinstance(space, spaces.MultiDiscrete):
        space_proto.space_type = "MultiDiscrete"
        space_proto.nvec.extend(space.nvec.tolist())
        space_proto.shape.extend(space.shape)
        space_proto.dtype = str(space.dtype)
    elif isinstance(space, spaces.MultiBinary):
        space_proto.space_type = "MultiBinary"
        space_proto.nvec.extend(list(space.shape))
        space_proto.shape.extend(space.shape)
        space_proto.dtype = str(space.dtype)
    else:
        # Raise an error for unsupported space types
        raise ValueError(f"Unsupported space type: {type(space).__name__}. "
                            f"Only Box, Discrete, MultiDiscrete, and MultiBinary spaces are supported.")

def native_to_numpy_space(proto_space):
    """Create a Gym action space from the protobuf space definition."""
    if proto_space.space_type == "Box":
        # Create a Box space
        low = np.array(proto_space.low, dtype=np.float32)
        high = np.array(proto_space.high, dtype=np.float32)
        shape = tuple(proto_space.shape)
        # Reshape the low and high arrays
        low = low.reshape(shape)
        high = high.reshape(shape)
        return spaces.Box(low=low, high=high, dtype=np.float32)
    elif proto_space.space_type == "Discrete":
        # Create a Discrete space with n possible actions
        return spaces.Discrete(proto_space.n)
    elif proto_space.space_type == "MultiDiscrete":
        # Create a MultiDiscrete space
        nvec = np.array(proto_space.nvec, dtype=np.int64)
        return spaces.MultiDiscrete(nvec)
    elif proto_space.space_type == "MultiBinary":
        # Create a MultiBinary space
        n = proto_space.nvec
        return spaces.MultiBinary(n)
    else:
        raise ValueError(f"Unsupported space type: {proto_space.space_type}")


def numpy_to_native(obj, space):
    """Convert numpy arrays and other non-serializable objects to serializable types
    based on the space.

    Args:
        obj: The object to convert
        space: The Gymnasium space object (Box, Discrete, MultiDiscrete, or MultiBinary)
    """
    # Handle the four base space types
    if isinstance(space, spaces.Discrete):
        return obj.item()
    else:
        return obj.tolist()

def native_to_numpy(obj, space):
    """Convert serialized objects back to their original form based on space.

    Args:
        obj: The object to convert
        space: The Gymnasium space object (Box, Discrete, MultiDiscrete, or MultiBinary)
    """
    if isinstance(space, spaces.Box):
        return np.array(obj, dtype=space.dtype).reshape(space.shape)
    elif isinstance(space, spaces.Discrete):
        return np.int64(obj)
    elif isinstance(space, spaces.MultiDiscrete):
        return np.array(obj, dtype=np.int64).reshape(space.shape)
    elif isinstance(space, spaces.MultiBinary):
        return np.array(obj, dtype=np.int8).reshape(space.shape)

def native_to_numpy_vec(obj, space, num_envs):
    """Convert serialized objects back to their original form based on space.

    Args:
        obj: The object to convert
        space: The Gymnasium space object (Box, Discrete, MultiDiscrete, or MultiBinary)
        num_envs: The number of environments
    """
    if isinstance(space, spaces.Box):
        return np.array(obj, dtype=space.dtype).reshape(num_envs, *space.shape)
    elif isinstance(space, spaces.Discrete):
        return np.array(obj, dtype=np.int64).reshape(num_envs, *space.shape)
    elif isinstance(space, spaces.MultiDiscrete):
        return np.array(obj, dtype=np.int64).reshape(num_envs, *space.shape)
    elif isinstance(space, spaces.MultiBinary):
        return np.array(obj, dtype=np.int8).reshape(num_envs, *space.shape)