from egat.shared_resource import SharedResource
from egat.testset import UnorderedTestSet
from egat.testset import SequentialTestSet
import time

# This example displays the capabilities of SharedResource decorators. By 
# decorating test classes and functions with their required resources the programmer
# can define which tests cannot be run at the same time other. For example, if two 
# tests need to log in as the same user and perform some action, they could define 
# a SharedResource to reflect that conflict. This signifies to other programmers and
# to the TestRunner that these tests cannot be run concurrently. 

# This SharedResource represents use of the application's database.
class ApplicationDatabaseResource(SharedResource):
    pass

# This SharedResource represents the use of the administrator's user account.
class AdminUserResource(SharedResource):
    pass

# This class tests the permissions for a certain web application. 
class PermissionsTests(UnorderedTestSet):
    def testManagerCanCreateUsers(self):
        assert(True)

    def testManagerCannotDeleteUsers(self):
        assert(True)

    # This method uses the Administrator User, who cannot be logged in in more than
    # one session. It is decorated with the AdminUserResource decorator to signify 
    # this.
    @AdminUserResource.decorator
    def testAdminCanCreateUsers(self):
        time.sleep(2)
        assert(True)

    # This method also uses the Administrator User. Since it is also decorated with 
    # the AdminUserResource, the TestRunner knows not to run this method at the same
    # time as any other tests with the AdminUserResource.
    @AdminUserResource.decorator
    def testAdminCanDeleteUsers(self):
        time.sleep(2)
        assert(True)

# This class tests the process of creating some object Foo.
# The tests in this class expect to have exclusive access to application's database
# so they are decorated with the ApplicationDatabaseResource decorator.
@ApplicationDatabaseResource.decorator
class TestFooCreation(SequentialTestSet):
    def testOpenFooPage(self):
        assert(True)

    def testClickCreateFooButton(self):
        assert(True)

    def testFooWasCreated(self):
        assert(True)

    # The testFooAuditLog test uses the Administrator username again, so it is 
    # decorated with the AdminUserResource decorator. It will not run at the same
    # time as the other methods with the AdminUserResource decorator.
    @AdminUserResource.decorator
    def testFooAuditLog(self):
        time.sleep(2)
        assert(True)
