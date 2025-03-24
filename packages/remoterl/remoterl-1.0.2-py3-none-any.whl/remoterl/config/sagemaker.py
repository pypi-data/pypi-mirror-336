from dataclasses import dataclass, asdict
from typing import Optional, Dict

CURRENT_REMOTE_RL_VERSION = "latest"  # Current Image Tag in ACCESIBLE_REGIONS

def get_image_uri(region: str) -> str:
    return f"533267316703.dkr.ecr.{region}.amazonaws.com/remoterl:{CURRENT_REMOTE_RL_VERSION}"

@dataclass
class SageMakerConfig:
    DEFAULT_ROLE_ARN = "arn:aws:iam::<your-aws-account-id>:role/SageMakerExecutionRole"
    DEFAULT_OUTPUT_PATH = "s3://<your-output-path>/"
    DEFAULT_REGION = "<your-aws-region>"
    BASE_REGION = "ap-northeast-2"
    
    role_arn: Optional[str] = DEFAULT_ROLE_ARN
    output_path: Optional[str] = DEFAULT_OUTPUT_PATH
    region: Optional[str] = DEFAULT_REGION
    instance_type: str = "ml.g5.4xlarge"
    instance_count: int = 1
    max_run: int = 3600

    def to_dict(self) -> Dict:
        """Returns a nested dictionary of the full SageMaker configuration."""
        return asdict(self)
    
    def set_config(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                print(f"Warning: No attribute '{k}' in SageMakerConfig")