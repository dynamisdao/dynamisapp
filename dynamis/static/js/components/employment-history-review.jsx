import React from 'react';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import uuid from 'uuid';

export default React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() {
    return {};
  },
  render() {
    return (
      <div className="card">
        <input name="group1" value="yes" type="radio" id="radio-input1" onChange={this.changeRadio} />
        <label htmlFor="radio-input1">Verify</label>
        <input name="group1" value="no" type="radio" id="radio-input2" onChange={this.changeRadio} />
        <label htmlFor="radio-input2">Falsify</label>
        <input name="group1" value="null" type="radio" id="radio-input3" onChange={this.changeRadio} />
        <label htmlFor="radio-input3">Can't Tell</label>
        <p>Here is copy on how to verify this person's employment history records.</p>
        <em>{this.props.notes}</em>
        company: {this.props.company} <br />
        dates: {new Date(this.props.startYear, this.props.startMonth).toString()} - {new Date(this.props.endYear, this.props.endMonth).toString()}
        {this.renderSigning()}
      </div>
    );
  },
  renderSigning() {
    if(this.state.result !== undefined) {
      var a = uuid.v4();
      return (
        <div className="input-field">
          <textarea className="materialize-textarea" valueLink={this.linkState('reason')} id={a}/>
          <label htmlFor={a}>Reason</label>
          please sign this:
          <code style={{wordWrap: 'break-word'}}>
            {JSON.stringify({
              task_hash: 'things',
              result: this.state.result,
              reason: this.state.reason
            })}
          </code>
          <textarea className="materialize-textarea" valueLink={this.linkState('signature')} />
          <button className="btn" onClick={() => this.props.submitReview(this.state.signature)}>Submit</button>
        </div>
      );
    }
  },
  changeRadio(e) {
    var value = e.target.value;
    if(value == 'null') value = null;
    this.setState({result: value});
  },
});
