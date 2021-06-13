import os
import subprocess

from app_config.database import app # , cache


class AdminService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Admin Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.file_path = '..'+os.sep+'data'+os.sep+'db'+os.sep+'covid19data.sql'
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [app_web] Admin Service [ready]")

    def database_dump(self):
        app.logger.info(" AdminService.database_dump() [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(os.getcwd())
        user = app.config['SQLALCHEMY_DATABASE_USER']
        url = app.config['SQLALCHEMY_DATABASE_HOST']
        db = app.config['SQLALCHEMY_DATABASE_DB']
        cmd = 'pg_dump --if-exists --clean --no-tablespaces '\
              +' --on-conflict-do-nothing --rows-per-insert=1000 --column-inserts '\
              +' --quote-all-identifiers --no-privileges -U '+user+' -h '+url+' '+db+' > '\
              + self.file_path
        app.logger.info(" start: "+str(cmd))
        returncode = self.__run_ome_shell_command(cmd)
        app.logger.info(" result: " + str(returncode))
        app.logger.info(" AdminService.database_dump() [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    @classmethod
    def __run_ome_shell_command(cls, cmd):
        args = [cmd]
        app.logger.info(" start: " + str(cmd))
        returncode = 0
        try:
            result = subprocess.run(args, shell=True, check=True, capture_output=True, encoding='UTF-8')
            returncode = result.returncode
        except subprocess.CalledProcessError as error:
            app.logger.warning("---------------------------------------------------------")
            app.logger.warning("  WARN:  AdminService.__run_ome_shell_command")
            app.logger.warning("---------------------------------------------------------")
            app.logger.warning("  cmd:    :::" + cmd + ":::")
            app.logger.warning("  erro:   :::" + str(error) + ":::")
            app.logger.warning("---------------------------------------------------------")
        return returncode

    def database_dump_reimport(self):
        app.logger.info(" AdminService.database_dump_reimport() [begin]")
        app.logger.info("------------------------------------------------------------")
        user = app.config['SQLALCHEMY_DATABASE_USER']
        url = app.config['SQLALCHEMY_DATABASE_HOST']
        db = app.config['SQLALCHEMY_DATABASE_DB']
        one_cmd = 'psql -U ' + user + ' -h ' + url + ' ' + db + ' < ' + self.file_path
        cmd_list = [
            one_cmd
        ]
        for cmd in cmd_list:
            returncode = self.__run_ome_shell_command(cmd)
            msg = '[ returncode: ' + str(returncode) + '] ' + cmd
            app.logger.info(msg)
        app.logger.info(" AdminService.database_dump_reimport() [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def database_drop_and_create(self):
        app.logger.info(" AdminService.database_drop_and_create() [begin]")
        app.logger.info("------------------------------------------------------------")
        with app.app_context():
            cache.clear()
            self.__database.drop_all()
            self.__database.create_all()
        app.logger.info("")
        app.logger.info(" AdminService.database_drop_and_create() [begin]")
        app.logger.info("------------------------------------------------------------")
        return self