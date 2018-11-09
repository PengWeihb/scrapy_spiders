


可以用shell模式进行命令的解析
scrapy shell http://www.baiud.com

css选择器
.css('a')   选取a节点
.css('.a')  选取class=a的节点
.css('a[href="ok"] img') 选取a属性为ok的a节点下的img节点
.css('a::text') 提取文本
.css('a::attr(href)') 提取属性

xpath选择器
.xpath('//a/@href')  提取所有a节点的属性值
.xpath('//a/text()') 提取所有a节点下的文字
.xpath('//a[@href="ok"]/text()')  提取属性为ok的a节点下的值


Selector对象常用方法
extract()
extract_first(default_value)
re((.*)name)  匹配(.*)name的正则,输出(.*)匹配上的数据
re_first((.*)name)


Downloader Middleware
process_request(request, spider)
None：    继续调用低优先级对的中间级
request： 低优先级的中间件不会再被调用，这个request被放回调度队列，等待重新调用
response：低优先级的中间件不会被调用，转而依次调用process_response

process_response(request, response, spider)
request:低优先级的中间件不会再被调用，这个request被放回调度队列，等待重新调用
response:继续被低优先级的中间件调用

process_exception(request, exception, spider)

Spider Middleware









Response
.body 获取bytes的返回内容
.text 获取返回的字符串


通过SchedulerMgr进行调度的request只能使用默认的回调



