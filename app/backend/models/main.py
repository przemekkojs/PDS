import lightgbm as lgb
from datetime import datetime
from .utils import retrain, process_row

LAST_TRAIN_TIME = datetime.now()
buffer_window = []
fee_model = lgb.Booster(model_file="contents/pred_fee.txt")
time_model = lgb.Booster(model_file="contents/pred_time.txt")