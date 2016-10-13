import React from 'react';
import {connectRedux} from '../utils';
import IdentityReview from './identity-review';
import EmploymentHistoryReview from './employment-history-review';
import _ from 'lodash';
import actions from '../actions/actions';
import NotificationPanel from './notification-panel';

export default connectRedux(React.createClass({
  componentDidMount() {
    this.props.dispatch(actions.loadP2PQueue());
  },
  render() {
    return (
      <div className="container">
        <NotificationPanel sectionId="review"/>
        <div className="row">
          <div className="col s6">
            <ul className="collection with-header">
              <li className="collection-header"><h4>P2P Task Queue</h4></li>
              {this.props.store.queue.tasks.map(this.renderTaskList)}
            </ul>
          </div>
          <div className="col s6">
            {this.renderTask()}
          </div>
        </div>
      </div>
    );
  },
  renderTask() {
    if(this.props.store.queue.selectedTask === null) { return null; }
    var task = this.props.store.queue.tasks[this.props.store.queue.selectedTask];
    var Component = {
      'employment-claim': EmploymentHistoryReview,
      identity: IdentityReview,
    }[task.type];
    return <Component {...task.data} submitReview={(signature) => this.props.dispatch(actions.submitReview(task.id, signature))} />;
  },
  renderTaskList(task, index) {
    return (
      <li className="collection-item" key={index}>
        <div>
          Verify {_.capitalize(task.type)}
          <i onClick={() => this.selectTask(index)} className="material-icons secondary-content cursor-pointer">send</i>
        </div>
      </li>
    );
  },
  selectTask(n) {
    this.props.dispatch(actions.setOn('queue', 'selectedTask', n));
  },
}));
