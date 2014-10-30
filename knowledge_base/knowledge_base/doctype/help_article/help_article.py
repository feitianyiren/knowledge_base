# Copyright (c) 2013, Web Notes and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import get_comment_list
from knowledge_base.utils import get_level_class, get_category_sidebar

class HelpArticle(WebsiteGenerator):
	condition_field = "published"
	template = "templates/generators/help_article.html"
	parent_website_route_field = "category"
	page_title_field = "title"

	def on_update(self):
		cnt = frappe.db.sql("""select count(*) from `tabHelp Article` where category=%s""", self.category)[0][0]
		frappe.db.set_value("Help Category", self.category, "help_articles", cnt)
		frappe.cache().delete_value("kb:category_sidebar")

	def get_context(self, context):
		context.login_required = True
		context.level_class = get_level_class(self.level)
		context.comment_list = get_comment_list(self.doctype, self.name)
		context.children = get_category_sidebar()

	def get_parents(self, context):
		return [{"title":"Knowledge Base", "name":"kb"}] + super(HelpArticle, self).get_parents(context)