import lightgbm as lgb
import pandas as pd

class ModelFineTuner:
    def __init__(self,model_path: str):
        """
        Initialize the fine-tuner by loading an existing trained LightGBM model.
        :param model_path: Path to the existing model file (e.g., lightgbm_model.txt).
        """
        self.model_path = model_path
        # Load the existing model to continue training from its current weights (warm-start)
        self.model = lgb.Booster(model_file=model_path)

    def fine_tune(self, X_new: pd.DataFrame, y_new: pd.Series, learning_rate: float = 0.01, num_boost_round: int = 50) -> lgb.Booster:
        """
        Perform incremental training (fine-tuning) on new incoming data using the existing model as a base.
        """

        # Prepare the new dataset in LightGBM binary format
        train_data = lgb.Dataset(X_new, label=y_new)

        # Continue training (warm-start) using init_model parameter
        # This allows the model to adapt to hardware degradation or new operating patterns without training from scratch
        updated_model = lgb.train(
            params={
                'learning_rate': learning_rate,
                'objective': 'regression',
                'metric': 'rmse'
            },
            train_set=train_data,
            num_boost_round=num_boost_round,
            init_model=self.model
        )

        # Update current reference
        self.model = updated_model
        return self.model

    def save_updated_model(self, output_path: str):
        """
        Save the re-weighted model back to disk.
        """
        self.model.save_model(output_path)
