import expect from 'expect';
import KeyBaseService from './keybase-service';

var services = {
  KeyBaseService: KeyBaseService,
  MockKeyBaseService: TestMocks.MockKeyBaseService
};

for(var serviceName in services) {
  var service = services[serviceName];
  describe(serviceName, function() {
    it('parses keybase information', function(done) {
      var promise = service.lookupUser('pipermerriam');
      promise.then(function(data) {
        expect(data.username).toEqual('pipermerriam');
        expect(data.twitter).toEqual('pipermerriam');
        done();
      }, function(status) {
        expect('keybase error').toEqual(status);
      });
    });

    it('handles the error', function(done) {
      var promise = service.lookupUser('pipermerriam1982381276368723687');
      promise.then(function(data) {
        expect('keybase didnt error out').toEqual('pipermerriam1982381276368723687');
      }, function(status) {
        expect(status.code).toNotEqual(0);
        done();
      });
    });
  });
}
