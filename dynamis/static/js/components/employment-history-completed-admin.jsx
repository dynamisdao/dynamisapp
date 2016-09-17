import React from 'react';
import {connectRedux} from '../utils';

export default connectRedux(React.createClass({
    render() {
        var monthNames = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ];
        return (
            <div className="card">
                <ul className="collection">
                    <li className="collection-item">
                        From: {monthNames[this.props.jobData.startMonth]} {this.props.jobData.startYear}</li>
                    <li className="collection-item">
                        To: {monthNames[this.props.jobData.endMonth]} {this.props.jobData.endYear}</li>
                    <li className="collection-item">Notes: {this.props.jobData.notes}</li>
                    <li className="collection-item">Company: {this.props.jobData.company}</li>
                </ul>
            </div>
        );
    },
}));
