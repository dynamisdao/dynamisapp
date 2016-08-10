import urls from '../urls';
import types from './types';
import {dispatchDjangoErrorMessages} from '../utils';

export function addEmploymentHistoryJob() {
  return {
    type: types.ADD_EMPLOYMENT_HISTORY_JOB
  };
}

export function updateEmploymentHistoryJob(jobId, field, value) {
  return {
    type: types.UPDATE_EMPLOYMENT_HISTORY_JOB,
    jobId: jobId,
    field: field,
    value: value
  };
}

export function validateEmploymentHistoryJob(jobId) {
  return function(dispatch, getState) {
    var target = 'job_' + jobId;
    dispatch({
      type: types.CLEAR_NOTIFICATIONS,
      target: target,
    });
    var job = getState().employmentHistory.jobs[jobId].current;
    var start = new Date(parseInt(job.startYear), parseInt(job.startMonth));
    var end = new Date(parseInt(job.endYear), parseInt(job.endMonth));
    if(start > end) {
      dispatch({
        type: types.ADD_NOTIFICATION,
        target: target,
        level: 'ERROR', // TODO
        message: 'start date must come before the end date',
        dismissable: false,
        uuid: target,
      });
    }
    return Promise.resolve();
  };
}

export function addFileToEmploymentHistory(jobId, name, mimetype, dataURL) {
  return function(dispatch, getState) {
    var store = getState();
    var policyId = store.policy.id;
    $.ajax({
      url: urls['policy-create'] + policyId + '/upload-file/',
      method: 'POST',
      data: JSON.stringify({
        filename: name,
        mimetype: mimetype,
        data_url: dataURL,
      }),
      contentType: 'application/json',
    }).done(data => {
      dispatch({
        type: types.ADD_EMPLOYMENT_HISTORY_JOB_FILE,
        jobId: jobId,
        ipfsHash: data.ipfs_hash,
        name: data.meta.name,
        mimetype: data.meta.mimetype,
      });
    }).error(response => {
      dispatchDjangoErrorMessages(dispatch, 'job_' + jobId, response.responseJSON);
    });
  };
}

export function removeFileFromEmploymentHistory(jobId, fileId) {
  return {
    type: types.REMOVE_EMPLOYMENT_HISTORY_JOB_FILE,
    jobId: jobId,
    fileId: fileId,
  };
}

export function toggleEmploymentHistoryEdit(jobId) {
  return {
    type: types.TOGGLE_EMPLOYMENT_HISTORY_EDIT,
    jobId: jobId,
  };
}

export function discardEmploymentHistoryChanges(jobId) {
  return {
    type: types.DISCARD_EMPLOYMENT_HISTORY_CHANGES,
    jobId: jobId,
  };
}

export function markEmploymentHistoryDone() {
  return {
    type: types.MARK_EMPLOYMENT_HISTORY_DONE,
  };
}

export function markEmploymentHistoryNotDone() {
  return {
    type: types.MARK_EMPLOYMENT_HISTORY_NOT_DONE,
  };
}

export function removeEmploymentHistoryJob(jobId) {
  return {
    type: types.REMOVE_EMPLOYMENT_HISTORY_JOB,
    jobId: jobId,
  };
}
