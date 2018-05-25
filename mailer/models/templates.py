from datetime import datetime
from typing import Union

from flask import flash

from mailer.models import Queue, Templates


class TemplateManager(object):

    @classmethod
    def add_template(cls, name: str, body: str, expires: str) -> bool:
        try:
            if expires != '':
                Templates(name=name, body=body, added=datetime.utcnow(), expires=expires)
            else:
                Templates(name=name, body=body, added=datetime.utcnow())
            return True
        except Exception as err:
            print(err)
            return False

    @classmethod
    def remove_template(cls, template_id: int) -> bool:
        if Queue.exists(template_id=template_id):
            flash("Can't delete template when customers in queue require it.", 'template_error')
            return False
        else:
            try:
                if Templates.exists(template_id=template_id):
                    tpl = Templates[template_id]
                    tpl.delete()
                    return True
                else:
                    return False
            except Exception as err:
                print(err)
                return False

    @classmethod
    def update_template(cls, template_id: int, name: str, body: str, expires: str) -> bool:
        try:
            if Templates.exists(template_id=template_id):
                tpl = Templates[template_id]
                tpl.name = name
                tpl.body = body
                if expires != "":
                    tpl.expires = expires
                else:
                    tpl.expires = None
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

    @classmethod
    def get_template(cls, template_id: int) -> Union[dict, bool]:
        try:
            if Templates.exists(template_id=template_id):
                return Templates[template_id]
            else:
                return False
        except Exception as err:
            print(err)
            return False

    @classmethod
    def get_templates(cls) -> dict:
        try:
            return Templates.select(lambda t: t.template_id > 0)[:]
        except Exception as err:
            print(err)
            return {}
