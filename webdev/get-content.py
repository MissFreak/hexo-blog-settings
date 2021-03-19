import os
import re
import itertools
file_path = r'D:\project\hexo-final\source\_posts'
# weblink = 'https://github.com/MissFreak/writings/blob/main/'
weblink = 'http://nlpcourse.cn/'
lst = os.listdir(file_path)
post_list = []
md_name = 'all-posts.md'
# md_name = 'README.md'

# obtain the titles and categories of all posts
for filename in lst:
	# make sure it is a markdown file
	if filename[-3:] == '.md':
		with open(os.path.join(file_path, filename), encoding="utf-8") as f:
			s = f.read()

		# create a dict that stores attributes: title and category_1 and category_2
		post_dict = {}

		# get the title
		match_title = re.search(r'(?<=title: ).*(?=\n)', s)
		if match_title:
			title = match_title.group().strip('"')
		else:
			title = filename

		# convert into linked title
		# linked_title = '[{}]({}{})'.format(title, weblink, filename)
		linked_title = '[{}]({}{})'.format(title, weblink, filename[:-3])

		# get the categories
		match_categories = re.search(r'categories:\n- (.*)\n- (.*)\n', s)
		try:
			category_1 = match_categories.group(1)
			category_2 = match_categories.group(2)
		except:
			category_1 = '未分类'
			category_2 = '未分类'

		# save into a list
		post_dict['title'] = linked_title
		post_dict['category_1'] = category_1
		post_dict['category_2'] = category_2
		post_list.append(post_dict)

# sort and group by the first category
get_first_category = lambda dct: dct.get('category_1')
group_1 = itertools.groupby(sorted(post_list, key=get_first_category), get_first_category)
num_post = len(post_list)

content = '---\ntitle: 所有文章目录\n---\n<center>目前共有{}篇文章：</center>\n<!-- more -->\n\n'.format(num_post)
for k1,v1 in group_1:
	# add the first category into content
	content += ('# '+k1+'\n')
	# sort and group by the first category
	get_second_category = lambda dct: dct.get('category_2')
	group_2 = itertools.groupby(sorted(v1, key=get_second_category), get_second_category)
	for k2,v2 in group_2:
		# add the second category into content
		if k2 != '未分类':
			content += ('- _'+k2+'_\n')
			for i in v2:
				# add the title into content
				content += ('\t- '+i['title']+'\n\n')
		else:
			for i in v2:
				# add the title into content
				content += ('- '+i['title']+'\n\n')
print(content)
# write the content into md file
with open(os.path.join(file_path, md_name), 'w', encoding='utf-8') as f:
	f.write(content)