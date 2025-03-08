# Import models so they get registered correctly
from .user import User
from .employee import Employee
from .payroll import Payroll
from .attendance import Attendance
from .company import Company

from .department import Department
from .payroll import Payroll, PayrollBenefit, PayrollOtherDeduction, PayrollReport
from .leave import Leave, LeaveAllocation, LeaveEntitlement

from .holiday import Holiday, HolidayType
from .role import Role