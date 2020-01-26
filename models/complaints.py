from datetime import datetime

from sqlite3 import IntegrityError
from controllers.core import Core
from controllers.login import Login


class Complaints:

    def __init__(self, user_id, bdo_user_id, gpm_user_id, complain_subject, complain_description):
        """
        An init function that is called when the class object is created. It also initializes the Class Variable
        :param user_id: User ID of Logged In user
        :param bdo_user_id: User ID of the BDO Current User reports to
        :param gpm_user_id: User ID of the GPM Current User reports to
        :param complain_subject: Subject of Complaint/Issue
        :param complain_description: Description of the Complaint/Issue
        """
        self.user_id = user_id
        self.bdo_user_id = bdo_user_id
        self.gpm_user_id = gpm_user_id
        self.complain_subject = complain_subject
        self.complain_description = complain_description
        self.bdo_remarks = None
        self.gpm_remarks = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_resolved = False

    def issue_complaints(self, conn):
        """
        function to insert a record in the member_complaints table, thereby filing a new complaint
        :param self: reference to the current object reference
        :param conn: a sqlite db connection object
        :return: new complaint_id of the record created
        """
        try:
            sql_query = '''INSERT INTO member_complaints(user_id, bdo_user_id, gpm_user_id, complain_subject, complain_description, bdo_remarks, gpm_remarks, created_at, updated_at, is_resolved) VALUES(?,?,?,?,?,?,?,?,?,?)'''
            sql_params = (self.user_id, self.bdo_user_id, self.gpm_user_id, self.complain_subject, self.complain_description, self.bdo_remarks, self.gpm_remarks, self.created_at, self.updated_at, self.is_resolved, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            member_complaints_id = cursor_obj.lastrowid
            cursor_obj.close()
            return member_complaints_id
        except IntegrityError:
            print(IntegrityError)

    @staticmethod
    def view_specific_complaints(conn, **kwargs):
        """
        a function to fetch the records from the member_complaints table in the database based on the role of the
        logged in user.
        :param conn: a sqlite db connection object
        :param kwargs: a keyword argument variable in case of update
        :return: a list of complaints.
        """
        action = kwargs.get('action', None)
        sql_query_complaints = str()
        if Login.logged_in_user['role'] == 'bdo':
            sql_query_complaints = '''SELECT * FROM member_complaints WHERE bdo_user_id=?'''
        elif Login.logged_in_user['role'] == 'gpm':
            sql_query_complaints = '''SELECT * FROM member_complaints WHERE gpm_user_id=?'''
        elif Login.logged_in_user['role'] == 'member':
            sql_query_complaints = f'''SELECT * FROM member_complaints WHERE user_id=?'''
        sql_params_complaints = (Login.logged_in_user['user_id'],)
        if not action == 'update':
            sql_query_complaints = sql_query_complaints + ''' AND is_resolved=False'''
        cursor_obj_complaints = Core.query_runner(conn, sql_query_complaints, sql_params_complaints)
        complaints = cursor_obj_complaints.fetchall()
        cursor_obj_complaints.close()
        return complaints

    @staticmethod
    def get_members_bdo_gpm(conn):
        """
        a function to fetch the user reporting heads of the logged in member
        :param conn: a sqlite db connection object
        :return: a dictionary of reporting heads of logged in member
        """
        sql_query_gpm = '''SELECT * FROM gpm_mem_rel WHERE mem_user_id=?'''
        sql_params_gpm = (Login.logged_in_user['user_id'],)
        cursor_obj_gpm = Core.query_runner(conn, sql_query_gpm, sql_params_gpm)
        mem_gpm_rel = cursor_obj_gpm.fetchone()
        cursor_obj_gpm.close()
        sql_query_bdo = '''SELECT * FROM bdo_gpm_rel WHERE gpm_user_id=?'''
        sql_params_bdo = (mem_gpm_rel['gpm_user_id'], )
        cursor_obj_bdo = Core.query_runner(conn, sql_query_bdo, sql_params_bdo)
        mem_bdo_rel = cursor_obj_bdo.fetchone()
        cursor_obj_bdo.close()
        mem_reporting_heads = dict()
        mem_reporting_heads['user_id'] = Login.logged_in_user['user_id']
        mem_reporting_heads['bdo_user_id'] = mem_bdo_rel['bdo_user_id']
        mem_reporting_heads['gpm_user_id'] = mem_gpm_rel['gpm_user_id']
        return mem_reporting_heads
