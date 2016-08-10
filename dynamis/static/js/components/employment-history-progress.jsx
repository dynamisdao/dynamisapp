import React from 'react';
import _ from 'lodash';

export default React.createClass({
  render() {
    var today = new Date();
    var thisYear = today.getFullYear();
    var validJobRanges = this.getValidJobRanges();
    return (
      <div className="card">
        <table className="bordered">
          <tbody>
            {[thisYear - 4, thisYear - 3, thisYear - 2, thisYear - 1, thisYear].map(function(year) {
              return (
                <tr key={year}>
                  <td>{year}</td>
                  {[0,1,2,3,4,5,6,7,8,9,10,11].map(function(month) {
                    var thisDate = new Date(year, month);
                    var isCovered = _.some(validJobRanges, job => (job.start <= thisDate && job.end >= thisDate) );
                    return (
                      <td key={year.toString() + month.toString()} className={isCovered ? 'light-green lighten2' : ''} >
                        {thisDate.toLocaleString('en-us', {month: 'long'})}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  },
  shouldComponentUpdate(nextProps) {
    function mapper(job) {
      return {
        startYear: job.current.startYear,
        startMonth: job.current.startMonth,
        endYear: job.current.endYear,
        endMonth: job.current.endMonth,
      };
    }
    var jobs1 = _.cloneDeep(this.props.jobs).map(mapper);
    var jobs2 = _.cloneDeep(nextProps.jobs).map(mapper);
    return !_.isEqual(jobs1, jobs2);
  },
  getValidJobRanges() {
    return _(this.props.jobs)
      .chain()
      .map('current')
      .map(function(job) {
        return {
          start: new Date(parseInt(job.startYear), parseInt(job.startMonth)),
          end: new Date(parseInt(job.endYear), parseInt(job.endMonth)),
        };
      }).filter(function(job) {
        return job.start <= job.end;
      }).value();
  },
});
