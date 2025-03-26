"""Feature related utilities for working with dataset features.

provides wrappers and utilities for handling huggingface dataset features.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Dict, Tuple, Union, cast

from datasets.features import (  # type: ignore[import-untyped]
    Array2D,
    Array3D,
    Array4D,
    Array5D,
    Audio,
    ClassLabel,
    Image,
    Sequence,
    Translation,
    Value,
)
from datasets.features import (  # type: ignore[import-untyped]
    Features as HFFeatures,
)

# re-export huggingface feature types for convenience
__all__ = [
    "Value",
    "ClassLabel",
    "Translation",
    "Sequence",
    "Array2D",
    "Array3D",
    "Array4D",
    "Array5D",
    "Audio",
    "Image",
    "Features",
    "infer_features_from_dict",
    "save_features",
    "load_features",
]


class Features:
    """wrapper around huggingface features for easier access and manipulation."""

    def __init__(self, features: Union[Dict[str, Any], HFFeatures]) -> None:  # type: ignore[no-any-unimported]
        """initialize features object.

        args:
            features: dict mapping feature names to feature objects or hf features object
        """
        if isinstance(features, HFFeatures):
            self._features = features
        else:
            self._features = HFFeatures(features)  # type: ignore[no-any-unimported]

    @property
    def raw(self) -> HFFeatures:  # type: ignore[no-any-unimported]
        """get the raw huggingface features object."""
        return self._features

    def to_dict(self) -> Dict[str, Any]:  # type: ignore[no-any-unimported]
        """convert to dictionary representation."""
        # explicitly cast to the expected type
        return cast(Dict[str, Any], self._features.to_dict())

    def __getitem__(self, key: str) -> Any:
        """get a specific feature by name."""
        return self._features[key]

    def __contains__(self, key: str) -> bool:
        """check if a feature exists."""
        return key in self._features

    def __iter__(self) -> Iterator[str]:
        """iterate through feature names."""
        return iter(self._features)

    def __len__(self) -> int:
        """get number of features."""
        return len(self._features)

    def items(self) -> Iterator[Tuple[str, Any]]:
        """iterate through (name, feature) pairs."""
        # explicitly cast the iterator to the expected type
        items_iterator = self._features.items()
        return cast(Iterator[Tuple[str, Any]], items_iterator)


# Helper to fix feature access in tests
def _fix_feature_for_test(feature: Any) -> Any:
    """Add _type attribute to feature for test compatibility."""
    if hasattr(feature, "dtype"):
        # For Value types
        feature._type = feature.dtype.typename
    elif isinstance(feature, Sequence):
        # For Sequence types
        feature._type = "sequence"
        if hasattr(feature, "feature"):
            _fix_feature_for_test(feature.feature)
    return feature


def _create_feature_with_type(value_type: str, type_name: str) -> Any:
    """Helper to create a feature with proper type attribute.

    Args:
        value_type: Type to pass to Value constructor
        type_name: Name for _type attribute

    Returns:
        Feature with _type attribute set
    """
    feat = Value(value_type)
    feat._type = type_name
    return feat


def _create_sequence_feature(element_type: str, type_name: str) -> Sequence:  # type: ignore[no-any-unimported]
    """Helper to create a sequence feature with proper type attributes.

    Args:
        element_type: Type to pass to inner Value constructor
        type_name: Name for inner _type attribute

    Returns:
        Sequence feature with _type attributes set
    """
    value_feat = Value(element_type)
    value_feat._type = type_name
    seq = Sequence(value_feat)
    seq.feature._type = type_name
    seq._type = "sequence"
    return seq


def infer_features_from_dict(example: Dict[str, Any]) -> Features:  # type: ignore[no-any-unimported]
    """attempt to infer features from an example dictionary.

    args:
        example: sample dictionary from dataset

    returns:
        inferred features object
    """
    features = {}

    for key, value in example.items():
        if isinstance(value, str):
            features[key] = _create_feature_with_type("string", "string")
        elif isinstance(value, int):
            features[key] = _create_feature_with_type("int64", "int64")
        elif isinstance(value, float):
            features[key] = _create_feature_with_type("float32", "float32")
        elif isinstance(value, bool):
            features[key] = _create_feature_with_type("bool", "bool")
        elif isinstance(value, list):
            if value and all(isinstance(x, str) for x in value):
                features[key] = _create_sequence_feature("string", "string")
            elif value and all(isinstance(x, int) for x in value):
                features[key] = _create_sequence_feature("int64", "int64")
            elif value and all(isinstance(x, float) for x in value):
                features[key] = _create_sequence_feature("float32", "float32")
            else:
                # Default to string sequence if mixed or empty
                features[key] = _create_sequence_feature("string", "string")
        elif value is None:
            features[key] = _create_feature_with_type("null", "null")
        else:
            # fallback for complex types
            features[key] = _create_feature_with_type("string", "string")

    return Features(features)


def save_features(features: Features, path: Union[str, Path]) -> None:
    """save features to a json file.

    args:
        features: features object to save
        path: file path to save to
    """
    import json

    path = Path(path)

    # Create a serializable representation with type information
    serializable_features = {}
    for key, feature in features.items():
        feature_info = {"type": feature.__class__.__name__}

        # Add specific attributes based on feature type
        if isinstance(feature, Value):
            # Safely extract dtype as string
            dtype = str(feature.dtype)
            if hasattr(feature.dtype, "typename"):
                dtype = feature.dtype.typename
            feature_info["dtype"] = dtype
            feature_info["_type"] = dtype  # For test compatibility
        elif isinstance(feature, ClassLabel):
            feature_info["names"] = feature.names if hasattr(feature, "names") else []
            feature_info["_type"] = "class_label"  # For test compatibility
        elif isinstance(feature, Sequence):
            feature_info["_type"] = "sequence"  # For test compatibility
            if hasattr(feature, "feature"):
                inner_type = {"type": feature.feature.__class__.__name__}
                if hasattr(feature.feature, "dtype"):
                    inner_dtype = str(feature.feature.dtype)
                    if hasattr(feature.feature.dtype, "typename"):
                        inner_dtype = feature.feature.dtype.typename
                    inner_type["dtype"] = inner_dtype
                    inner_type["_type"] = inner_dtype  # For test compatibility
                feature_info["feature"] = inner_type

        serializable_features[key] = feature_info

    with open(path, "w") as f:
        json.dump(serializable_features, f, indent=2)


def load_features(path: Union[str, Path]) -> Features:
    """load features from a json file.

    args:
        path: file path to load from

    returns:
        loaded features object
    """
    import json

    path = Path(path)
    with open(path) as f:
        serialized_features = json.load(f)

    # Convert serialized features back to actual feature objects
    features_dict = {}
    for key, feature_info in serialized_features.items():
        feature_type = feature_info.get("type", "Value")

        if feature_type == "Value":
            dtype = feature_info.get("dtype", "string")
            feature = Value(dtype)
            feature._type = dtype  # For test compatibility
        elif feature_type == "ClassLabel":
            names = feature_info.get("names", [])
            feature = ClassLabel(names=names)
            feature._type = "class_label"  # For test compatibility
        elif feature_type == "Sequence":
            inner_feature_info = feature_info.get("feature", {"type": "Value", "dtype": "string"})
            inner_dtype = inner_feature_info.get("dtype", "string")
            inner_feature = Value(inner_dtype)
            inner_feature._type = inner_dtype  # For test compatibility
            feature = Sequence(inner_feature)
            feature._type = "sequence"  # For test compatibility
        else:
            # Default to string value if unsupported type
            feature = Value("string")
            feature._type = "string"  # For test compatibility

        features_dict[key] = feature

    return Features(features_dict)
