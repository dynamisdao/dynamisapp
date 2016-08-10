import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import FileIcon from './file-icon';

describe('FileIcon', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><FileIcon file={{}} /></Provider>);
  });
});
