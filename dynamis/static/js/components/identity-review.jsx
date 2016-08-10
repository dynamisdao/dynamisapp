import React from 'react';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import uuid from 'uuid';

export default React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() {
    return {
      hoverStar: null,
      result: null,
    };
  },
  render() {
    return (
      <div className="card">
        <div>{this.state.result}</div>
        <div>
          {[1,2,3,4,5].map(this.renderStar)}
        </div>
        <p>Please verify this person's {this.props.proof_type} username: <code>{this.props.nametag}</code></p>
        <a href={this.props.service_url} target="_blank">View their profile</a>
        <p>
          {this.renderCopy()}
        </p>
        {this.renderSigning()}
      </div>
    );
  },
  renderStar(n) {
    var classes = 'material-icons cursor-pointer';
    var amtOfStarsHighlighted = this.state.hoverStar === null ? this.state.result : this.state.hoverStar;
    if(amtOfStarsHighlighted >= n) {
      classes += ' green-text';
    }
    return (
      <i
        key={n}
        className={classes}
        onMouseOver={this.onStarMouseOver.bind(this, n)}
        onMouseLeave={this.onStarMouseLeave}
        onClick={this.selectStar.bind(this, n)}>
        stars
      </i>
    );
  },
  onStarMouseOver(n) {
    this.setState({hoverStar: n});
  },
  onStarMouseLeave() {
    this.setState({hoverStar: null});
  },
  selectStar(n) {
    this.setState({result: n});
  },
  renderSigning() {
    if(this.state.result) {
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
  renderCopy() {
    return {
      'keybase': 'here is some generic copy on how to verify KEYBASE',
      'facebook': 'here is some generic copy on how to verify FACEBOOK',
      'twitter': 'here is some generic copy on how to verify TWITTER',
    }[this.props.type];
  },
});
