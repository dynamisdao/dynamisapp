import React from 'react';
import expect from 'expect';
import ReactTestUtils from 'react-addons-test-utils';

import App from './app';

describe('App', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('should render an h1', function() {
    var component = ReactTestUtils.renderIntoDocument(<App store={this.store}/>);
    var amt = ReactTestUtils.scryRenderedDOMComponentsWithTag(component, 'h1').length;
    expect(amt).toEqual(1);
  });
});
