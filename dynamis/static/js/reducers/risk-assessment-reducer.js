// import types from '../actions/types';
import Reducer from './reducer';

var reducer = new Reducer('riskAssessment', {
  identities: [
    {
      data: {type: 'keybase', username: 'pipermarry\'em'},
      reviews: [{score: 5, reason: 'its good'},{score: 4, reason: 'nice'},{score: 5, reason: 'wow'}]
    },
    {
      data: {type: 'twitter', username: 'pipermarry\'em'},
      reviews: [{score: 1, reason: 'twitter sucks'},{score: 1, reason: 'i hate twitter'},{score: 2, reason: 'get back to work'}]
    },
    {
      data: {type: 'reddit', username: 'pipermarry\'em'},
      reviews: [{score: 4, reason: 'its ok'},{score: 4, reason: 'cool'},{score: 3, reason: 'hello reddit'}]
    },
  ],
  jobs: [
    {
      notes: 'its a job',
      company: 'job giver people',
      startYear: 2014,
      startMonth: 3,
      endYear: 2015,
      endMonth: 5,
    },
    {
      notes: 'its another job',
      company: 'job giver people employer other people beanfactory',
      startYear: 2015,
      startMonth: 6,
      endYear: 2015,
      endMonth: 10,
    },
  ],
  estimatedClaimLength: null,
  estimatedDaysThatClaimWontOpen: null,
  expanded: null,
});

reducer.addSetter('expanded');

export default reducer.build();
