import keybase from './keybase-reducer';
import account from './account-reducer';
import policy from './policy-reducer';
import wallet from './wallet-reducer';
import queue from './queue-reducer';
import employmentHistory from './employment-history-reducer';
import notifications from './notifications-reducer';
import riskAssessment from './risk-assessment-reducer';
import {combineReducers} from 'redux';

export default combineReducers({
  keybase: keybase,
  account: account,
  employmentHistory: employmentHistory,
  policy: policy,
  notifications: notifications,
  wallet: wallet,
  queue: queue,
  riskAssessment: riskAssessment,
});
