import types from '../actions/types';
import {removeIndexFromArray} from '../utils';
import {STATES} from '../constants';
import _ from 'lodash';
import Reducer from './reducer';

var reducer = new Reducer('employmentHistory', {
  done: false,
  jobs: [],
});

reducer.subscribe(types.ADD_EMPLOYMENT_HISTORY_JOB, function(state, action) {
  return {
    ...state,
    jobs: state.jobs.concat({
      saved: null,
      current: {
        files: [],
        state: STATES.NEW,
        notes: '* Job Title:\n* Reason for leaving:\n\nIn order to verify my employment at <COMPANY> you can contact <supervisor-name> who was my <SUPERVISOR/BOSS>.  They can be reached via <EMAIL-ADDRESS/PHONE-NUMBER>.  You can verify their position with the company by <INSERT-HOW-TO-VERIFY-THEIR-POSITION>.',
        currentJob: false,
      },
    })
  };
});

reducer.subscribe(types.UPDATE_EMPLOYMENT_HISTORY_JOB, function(state, action) {
  if(action.field === 'currentJob' && action.value) {
    var today = new Date();
    state.jobs[action.jobId].current.endMonth = today.getMonth();
    state.jobs[action.jobId].current.endYear = today.getFullYear();
  }
  state.jobs[action.jobId].current[action.field] = action.value;
  return {
    ...state,
    jobs: state.jobs
  };
});

reducer.subscribe(types.ADD_EMPLOYMENT_HISTORY_JOB_FILE, function(state, action) {
  state.jobs[action.jobId].current.files.push({
    name: action.name,
    mimetype: action.mimetype,
    ipfsHash: action.ipfsHash,
  });
  return {
    ...state,
    jobs: state.jobs
  };
});

reducer.subscribe(types.REMOVE_EMPLOYMENT_HISTORY_JOB_FILE, function(state, action) {
  state.jobs[action.jobId].current.files = removeIndexFromArray(state.jobs[action.jobId].current.files, action.fileId);
  return {
    ...state,
    jobs: state.jobs
  };
});

reducer.subscribe(types.DISCARD_EMPLOYMENT_HISTORY_CHANGES, function(state, action) {
  if (state.jobs[action.jobId].current.state === STATES.NEW) {
    state.jobs = removeIndexFromArray(state.jobs, action.jobId);
  } else {
    state.jobs[action.jobId].current = _.cloneDeep(state.jobs[action.jobId].saved);
    state.jobs[action.jobId].current.state = STATES.READ_ONLY;
  }
  return {
    ...state,
    jobs: state.jobs
  };
});

reducer.subscribe(types.TOGGLE_EMPLOYMENT_HISTORY_EDIT, function(state, action) {
  if (state.jobs[action.jobId].current.state === STATES.READ_ONLY) {
    state.jobs[action.jobId].current.state = STATES.EDITING;
  } else {
    state.jobs[action.jobId].current.state = STATES.READ_ONLY;
    state.jobs[action.jobId].saved = _.cloneDeep(state.jobs[action.jobId].current);
  }

  return {
    ...state,
    jobs: state.jobs
  };
});

reducer.subscribe(types.MARK_EMPLOYMENT_HISTORY_DONE, function(state, action) {
  return {
    ...state,
    done: true
  };
});

reducer.subscribe(types.MARK_EMPLOYMENT_HISTORY_NOT_DONE, function(state, action) {
  return {
    ...state,
    done: false
  };
});

reducer.subscribe(types.SET_POLICY_DATA, function(state, action) {
  var newJobs = action.jobs.map(function(job) {
    return { current: job, saved: _.cloneDeep(job) };
  });
  return {
    ...state,
    jobs: newJobs,
    done: newJobs.length > 0
  };
});

reducer.subscribe(types.REMOVE_EMPLOYMENT_HISTORY_JOB, function(state, action) {
  state.jobs = removeIndexFromArray(state.jobs, action.jobId);
  return {
    ...state,
    jobs: state.jobs
  };
});

export default reducer.build();
