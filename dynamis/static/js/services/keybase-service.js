import _ from 'lodash';

var URL = 'https://keybase.io/_/api/1.0/user/lookup.json';
var KeyBaseService = {
  lookupUser(username) {
    return new Promise(function(resolve, reject) {
      $.ajax({
        url: URL,
        data: { username: username },
        method: 'GET',
      }).always(function(data) {
        if(data.status.code === 0) {
          // on successful response, parse out the keybase data we want
          var parsed = {
            username: data.them.basics.username,
            picture: _.get(data, 'them.pictures.primary.url', 'https://keybase.io/images/no-photo/placeholder-avatar-180-x-180.png'),
            proofs: _.get(data, 'them.proofs_summary.all', []),
          };
          resolve(parsed);
        } else {
          // on unsuccessful response, give the status of the response
          reject(data.status);
        }
      });
    });
  },
};

export default KeyBaseService;
