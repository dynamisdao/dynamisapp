import types from '../actions/types';
import Reducer from './reducer';

var reducer = new Reducer('queue', {
  tasks: [],
  history: [],
  selectedTask :null,
});

reducer.subscribe(types.LOAD_P2P_QUEUE, function(state, action) {
  return {
    ...state,
    tasks: action.tasks,
    selectedTask: null,
  };
});

reducer.addSetter('history');
reducer.addSetter('selectedTask');

export default reducer.build();
