---
title: "前端 AI 自动化测试：brower-use 调研"
source: "https://zhuanlan.zhihu.com/p/1964966278700728839"
author:
  - "[[windliang​互联网行业 从业人员]]"
published:
created: 2026-03-20
description: "AI 发展比较快，公司组内分享于 9.23随着 Vibe Coding 的快速发展， Anthropic 官方演讲：Vibe Coding 如何用到线上正式项目中  中介绍的我们需要一个帮助我们验证系统正确性的工具。brower-use 为我们提供了一个…"
tags:
  - "clippings"
---
> AI 发展比较快，公司组内分享于 9.23

随着 Vibe Coding 的快速发展， [Anthropic 官方演讲：Vibe Coding 如何用到线上正式项目中](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/eVJtcqXrivivfOwWN_Y0_w) 中介绍的我们需要一个帮助我们验证系统正确性的工具。 [brower-use](https://zhida.zhihu.com/search?content_id=265483555&content_type=Article&match_order=1&q=brower-use&zhida_source=entity) 为我们提供了一个自动化测试的强有力的工具。

分 brower-use 和 AI 自动化测试两部分介绍：

## brower-use

## 项目概述

[Browser-Use](https://link.zhihu.com/?target=https%3A//docs.browser-use.com/introduction) 是一个开源的 Python 库，旨在让 AI 能够自主地与网页进行交互。

该项目允许用户通过自然语言描述任务，AI 通过 Chrome DevTools Protocol（CDP 协议） 执行 Chrome/Chromium 浏览器复杂的网页操作，如网页导航、表单填写、数据提取、在线购物等。

### 核心特性

- 纯文本任务描述：用户只需用自然语言描述任务，无需编写代码
- 自主浏览器操作：支持点击、输入、滚动、多标签页管理等全套浏览器操作
- 多模型支持：支持 OpenAI、Anthropic、Google、 [Azure](https://zhida.zhihu.com/search?content_id=265483555&content_type=Article&match_order=1&q=Azure&zhida_source=entity) 、 [Groq](https://zhida.zhihu.com/search?content_id=265483555&content_type=Article&match_order=1&q=Groq&zhida_source=entity) 、 [Ollama](https://zhida.zhihu.com/search?content_id=265483555&content_type=Article&match_order=1&q=Ollama&zhida_source=entity) 等多种大语言模型
- 实时屏幕截图：具备视觉理解能力，可以看到页面内容
- 跨平台支持：支持 Windows、macOS、Linux
- 云端服务：提供托管的云端解决方案
<video src="https://vdn6.vzuu.com/HD/a4c113d0-b06d-11f0-9206-2e374f181401-v8_f2_t1_oXiNvrEP.mp4?pkey=AAU9rEKrPrUvuWBq2ip_EaRkkKWamgp8l-C40Rg01xdV1kJU2w1jND6soaXwutqiAVIpG3h3TkrBSNEX91HPZMfy&amp;bu=1513c7c2&amp;c=avc.8.0&amp;expiration=1773948070&amp;f=mp4&amp;pu=e59e796c&amp;v=ks6&amp;pp=ChMxNDAxNjIzODY1NzM5NTc5MzkyGGMiC2ZlZWRfY2hvaWNlMhMxMzY5MDA1NjA4NTk5OTA0MjU3PXu830Q%3D&amp;pf=Web&amp;pt=zhihu"></video>![](https://picx.zhimg.com/v2-a8625d0882c51ec7f368299c69d4a096.jpg?source=25ab7b06)

00:59

本地安装时候需要镜像源：

安装 brower-use

> uv pip install -i [pypi.tuna.tsinghua.edu.cn](https://link.zhihu.com/?target=https%3A//pypi.tuna.tsinghua.edu.cn/simple) browser-use

安装 playwright

```bash
# 1) 把 uv 的包源指向清华镜像（PyPI 国内镜像）

export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 2) 拉长 http 超时时间（默认 30s 太短）

export UV_HTTP_TIMEOUT=600

# 3) 仍然使用淘宝的 Playwright 浏览器镜像

export PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"

# 4) 用 uvx 安装并拉浏览器（可指定版本，避免解析到别的版本）

uvx --index "$UV_INDEX_URL" playwright@1.55.0 install chromium --with-deps
```

### 核心原理

核心思想是一个 ReAct，可以看 [一文入门 agent：从理论到代码实战](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/EaKx526SE5nb-T9XgJlkNQ) 这篇文章介绍的。

![](https://pic2.zhimg.com/v2-902c4a16d45cdb4fb8d06f35d1fa7a3d_1440w.jpg)

## 使用示例

1. 基础搜索示例
```python
import asyncio
   from browser_use import Agent, ChatOpenAI
   
   async def main():
       agent = Agent(
           task="在 Google 上搜索 'browser automation' 并告诉我前 3 个结果",
           llm=ChatOpenAI(model="gpt-4o-mini"),
       )
       await agent.run()
   
   asyncio.run(main())
```
1. 在线购物示例
```python
# 复杂的购物任务
   task = """
   访问 Migros 在线商店，搜索以下商品并添加到购物车：
   
   - 牛肉末 (1kg)
   - 格鲁耶尔奶酪
   - 全脂牛奶 (2升)
   - 黄油
   - 胡萝卜 (1kg)
     完成购买流程并选择 TWINT 支付方式
     """
```
1. 多标签页操作
```bash
# 在多个标签页中执行任务
   
   task = "打开 3 个标签页分别搜索 Elon Musk、Sam Altman 和 Steve Jobs，然后返回第一个标签页"
```
1. 文件上传功能
```python
# 自定义文件上传工具
   
   @tools.action('上传文件到指定元素')
   async def upload_file(index: int, path: str, browser_session: BrowserSession):
       # 获取 DOM 元素
       dom_element = await browser_session.get_dom_element_by_index(index)
       # 执行文件上传
       event = browser_session.event_bus.dispatch(UploadFileEvent(node=dom_element, file_path=path))
       await event
```

## 应用场景

1. 自动化测试 （✅本文主要探讨的方向）
- UI 测试：自动化用户界面测试
- 回归测试：自动执行回归测试用例
- 性能测试：监控页面加载和响应时间
1. 数据采集
- 网页爬虫：智能网页数据抓取
- 竞品分析：自动收集竞争对手信息
- 市场调研：自动化市场数据收集
1. 业务流程自动化
- 表单填写：自动化表单处理
- 订单处理：自动化订单管理
- 客户服务：自动化客户支持流程
1. 个人助手应用
- 在线购物：智能购物助手
- 信息查询：自动化信息检索
- 账户管理：自动化账户操作

## GUI

### web-ui

[github.com/browser-use/](https://link.zhihu.com/?target=https%3A//github.com/browser-use/web-ui)

基于 brower-use 的一个可视化操作工具。

<video src="https://vdn6.vzuu.com/HD/bc220f48-b06d-11f0-801a-325417b1e40f-v8_f2_t1_jgqa2x2k.mp4?pkey=AAXRBj66cAyQ7HJRJ0rBkXs_zi7uYuQPKMN6dcddKfiL6EFEzWJPvEYVzvuJcKuxv5uLXGr0TNPxupZZlCxT0NNq&amp;bu=1513c7c2&amp;c=avc.8.0&amp;expiration=1773948070&amp;f=mp4&amp;pu=e59e796c&amp;v=ks6&amp;pp=ChMxNDAxNjIzODY1NzM5NTc5MzkyGGMiC2ZlZWRfY2hvaWNlMhMxMzY5MDA1NjA4NTk5OTA0MjU3PXu830Q%3D&amp;pf=Web&amp;pt=zhihu"></video>![](https://pica.zhimg.com/v2-20cb99ac1023e76a070f2b5c21b6fca0.jpg?source=25ab7b06)

00:24

### VibeSurf

[github.com/vvincent1234](https://link.zhihu.com/?target=https%3A//github.com/vvincent1234/VibeSurf)

基于 brower-use 和浏览器插件的可视化操作工具。

<video src="https://vdn6.vzuu.com/HD/c1cf13e6-b06d-11f0-b2fb-2e374f181401-v8_f2_t1_YoY72hCd.mp4?pkey=AAVhGZXDrD9X6ep-E6oC7gKM_HjZoRYZ3WxdFOWfu66GNvaqGQRSWWfQtAOLllLXNfjWuv0zHIDJYuiDjKzSW6rj&amp;bu=1513c7c2&amp;c=avc.8.0&amp;expiration=1773948070&amp;f=mp4&amp;pu=e59e796c&amp;v=ks6&amp;pp=ChMxNDAxNjIzODY1NzM5NTc5MzkyGGMiC2ZlZWRfY2hvaWNlMhMxMzY5MDA1NjA4NTk5OTA0MjU3PXu830Q%3D&amp;pf=Web&amp;pt=zhihu"></video>![](https://picx.zhimg.com/v2-abb5f5a1cf76453257b79abfc2a9c8a2.jpg?source=25ab7b06)

01:11

## AI 自动化测试

基于 brower-use，渐进式的可以有三个方向进行探索。

- prompt
- [MCP](https://zhida.zhihu.com/search?content_id=265483555&content_type=Article&match_order=1&q=MCP&zhida_source=entity)
- 一体化测试平台

## prompt

可参考 [awesome-prompts](https://link.zhihu.com/?target=https%3A//github.com/browser-use/awesome-prompts%3Ftab%3Dreadme-ov-file%23testing-and-qa-prompts) ，测试相关的：

### Website Functionality Testing

```python
Perform a comprehensive functionality test of {website} focusing on the {specific_feature} and core user journeys.

Test the following user flows:

1. User registration and login process
   - Create a new account with test credentials
   - Verify email confirmation process
   - Log out and log back in
   - Test password reset functionality

2. {specific_feature} functionality
   - Test all UI elements (buttons, forms, dropdowns)
   - Verify data entry and validation
   - Test error handling and messaging
   - Check performance under various conditions

3. Critical user journeys
   - {user_journey1} (e.g., product search to checkout)
   - {user_journey2} (e.g., account settings update)
   - {user_journey3} (e.g., content submission)

4. Cross-browser compatibility
   - Test core functionality on Chrome, Firefox, and Safari
   - Document any rendering or functionality differences

For each test, document:

- Test case description
- Expected behavior
- Actual behavior
- Screenshots of issues encountered
- Severity rating (Critical, High, Medium, Low)
```

### Responsive Design Testing

```python
Test the responsive design of {website} across various device types and screen sizes.

1. Test the following key pages:
   - Homepage
   - {page1} (e.g., product listing)
   - {page2} (e.g., product detail)
   - {page3} (e.g., checkout)
   - {page4} (e.g., account settings)

2. For each page, test the following screen sizes and orientations:
   - Mobile: 320px, 375px, 414px (portrait and landscape)
   - Tablet: 768px, 1024px (portrait and landscape)
   - Desktop: 1366px, 1920px

3. For each combination, evaluate:
   - Content visibility and readability
   - Navigation usability
   - Image and media scaling
   - Form functionality
   - Touch targets and interactive elements
   - Load time and performance

4. Test specific responsive features:
   - Hamburger menu functionality on mobile
   - Collapsible sections
   - Image carousels/sliders
   - Tables or complex data representations
   - Modal windows and popups

Document all issues with screenshots, device information, and recommended fixes. Prioritize issues based on severity and frequency of user encounter.
```

### User Registration Flow Testing

```python
Test the entire user registration flow on {website} to identify any usability issues or bugs.

1. Begin by navigating to the site's homepage and finding the registration option
2. Test the following registration methods:
   - Email registration
   - Google/social media account registration (if available)
   - Phone number registration (if available)

3. For email registration, test:
   - Form validation for each field
   - Password strength requirements
   - Email verification process
   - "Already registered" error handling

4. Document the following for each step:
   - Field requirements and validations
   - Error messages (clarity and helpfulness)
   - Number of steps in the process
   - Time taken to complete each step

5. Test edge cases:
   - Using an email that's already registered
   - Using invalid formats for fields
   - Abandoning the process mid-way and returning
   - Registering from different browsers or devices

6. After successful registration, verify:
   - Welcome email receipt and content
   - Initial account state and settings
   - Any onboarding processes or tutorials
   - Logout and login functionality with the new account

Provide a detailed report with screenshots of any issues found, along with severity ratings and suggestions for improvement.
```

### Accessibility Testing

```python
Conduct an accessibility test of {website} to identify issues that may impact users with disabilities.

1. Test keyboard navigation:
   - Tab through all interactive elements on key pages
   - Verify visible focus indicators
   - Test all functionality without using a mouse
   - Check for keyboard traps or inaccessible elements

2. Test screen reader compatibility:
   - Enable VoiceOver (Mac) or NVDA (Windows)
   - Navigate through key pages and verify all content is announced
   - Check for appropriate alt text on images
   - Verify form fields have proper labels
   - Test dynamic content updates

3. Test color contrast and visual presentation:
   - Check text contrast against backgrounds
   - Verify information is not conveyed by color alone
   - Test the site at 200% zoom
   - Verify the site works in high contrast mode

4. Test form and interactive elements:
   - Verify clear error messages
   - Check for appropriate input validation
   - Test timeout warnings and session management
   - Verify multimedia has captions or transcripts

5. Check against WCAG 2.1 AA standards:
   - Verify semantic HTML structure
   - Check for proper heading hierarchy
   - Test ARIA implementations
   - Verify appropriate landmark regions

Document all issues with screenshots, steps to reproduce, and references to relevant WCAG criteria.
```

## MCP

[github.com/browser-use/](https://link.zhihu.com/?target=https%3A//github.com/browser-use/vibetest-use)

<video src="https://vdn6.vzuu.com/HD/ccfe17bc-b06d-11f0-8bb2-0219d46f3c7f-v8_f2_t1_gMjpeMoF.mp4?pkey=AAWaOxiaM36f4tI13xp2sfRhmN97MvWQKMKo0KJ8Tf8uORbPDY3r8-6JvAfZM1amAxRWuJ9Nq4eUyXAabgu5-f-n&amp;bu=1513c7c2&amp;c=avc.8.0&amp;expiration=1773948070&amp;f=mp4&amp;pu=e59e796c&amp;v=ks6&amp;pp=ChMxNDAxNjIzODY1NzM5NTc5MzkyGGMiC2ZlZWRfY2hvaWNlMhMxMzY5MDA1NjA4NTk5OTA0MjU3PXu830Q%3D&amp;pf=Web&amp;pt=zhihu"></video>![](https://picx.zhimg.com/v2-9a2a8b29255e9e2cfa99d446ed1463f7.jpg?source=25ab7b06)

02:08

基于 AI 的自动化 QA 测试工具，专门用于测试 AI 生成的网站。使用多个 Browser-Use 智能代理来并行测试网站的 UI 缺陷、损坏的链接、可访问性问题和其他技术问题提供了一个 MCP，可以与 Claude 和 Cursor 等 AI 编程工具集成。

demo 性质，项目比较简单，一个 agent ，一个 mcp 。

![](https://pica.zhimg.com/v2-fd5e3eaf0ef2792c0ca0efbdf65a3204_1440w.jpg)

值得学习的还是 agents 中的 prompt，prompt 技巧可以参考 [Anthropic 官方提示词工程教程收获总结：Prompt 提示词工程快速入门](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/bFmmjmHP2We9NP8Reo3vzw) 。

```python
"""
You are an objective QA analyst. Review the following test reports from agents that explored the website {test_data['url']}.

Identify only actual functional issues, broken features, or technical problems. Do NOT classify subjective opinions, missing features that may be intentional, or design preferences as issues.

Only report issues if they represent:

- Broken functionality (buttons that don't work, forms that fail)
- Technical errors (404s, JavaScript errors, broken links)
- Accessibility violations (missing alt text, poor contrast)
- Performance problems (very slow loading, timeouts)

IMPORTANT: For each issue you identify, provide SPECIFIC and DETAILED descriptions including:

- The exact element that was tested (button name, link text, form field, etc.)
- The specific action taken (clicked, typed, submitted, etc.)
- The exact result or error observed (404 error, no response, broken redirect, etc.)
- Any relevant context from the agent's testing

DO NOT use vague descriptions like "broken link" or "404 error". Instead use specific descriptions like:

- "Upon clicking the 'Contact Us' button in the header navigation, the page redirected to a 404 error"
- "When submitting the newsletter signup form with a valid email, the form displayed 'Server Error 500' instead of confirmation"

Here are the test reports:
{bug_reports_text}

Format the output as JSON with the following structure:
{{
    "high_severity": [
        {{ "category": "category_name", "description": "specific detailed description with exact steps and results" }},
        ...
    ],
    "medium_severity": [
        {{ "category": "category_name", "description": "specific detailed description with exact steps and results" }},
        ...
    ],
    "low_severity": [
        {{ "category": "category_name", "description": "specific detailed description with exact steps and results" }},
        ...
    ]
}}

Only include real issues found during testing. Provide clear, concise descriptions. Deduplicate similar issues.
"""
```

## 一体化测试平台

[github.com/browser-use/](https://link.zhihu.com/?target=https%3A//github.com/browser-use/qa-use)

QA-Use 是一个基于 AI 的智能化端到端测试平台，让用户可以用自然语言描述测试场景（如”访问登录页面，输入用户名和密码，点击登录按钮”），然后由 AI 代理自动在真实浏览器中执行这些测试步骤。

平台支持测试套件的创建和管理、定时自动执行（每小时或每天）、实时监控测试过程、完整的执行历史追踪，以及测试失败时的邮件通知功能。

  

![](https://pic1.zhimg.com/v2-f2726465b54c09d3cbd185a3a6422d7c_1440w.jpg)

  

内部集成了 BrowserUse Cloud API ，直接使用需要收费，但整体项目的架构可以学习。

![](https://pic3.zhimg.com/v2-9d58fa369649e8e65f04110045627f80_1440w.jpg)

  

## 其他项目

### SDET-GENIE

[github.com/WaiGenie/SDE](https://link.zhihu.com/?target=https%3A//github.com/WaiGenie/SDET-GENIE)

将用户输入的简单想法自动生成综合的手工测试用例，通过智能浏览器代理在真实浏览器环境中执行测试并收集交互数据，最后生成支持多种主流框架（如Selenium、Playwright、Cypress等）的自动化代码。

用户输入： `As a user, I want to log in with valid credentials so that I can access my account.`

生成 case：

```bash
Feature: User Authentication

  @positive
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "standard_user" in the username field
    And I enter "secret_sauce" in the password field
    And I click the login button
    Then I should be redirected to the inventory page
    
  @negative
  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter "invalid_user" in the username field
    And I enter "wrong_password" in the password field
    And I click the login button
    Then I should see an error message
```

  

![](https://pic2.zhimg.com/v2-0473fde7fd761eecdcef1d0ed1151dff_1440w.jpg)

  

详细介绍的文章： [medium.com/@honeyricky1](https://link.zhihu.com/?target=https%3A//medium.com/%40honeyricky1m3/from-user-stories-to-automated-tests-the-future-of-qa-automation-using-ai-agents-cfe7fe878954)

### web-eval-agent

[github.com/Operative-Sh](https://link.zhihu.com/?target=https%3A//github.com/Operative-Sh/web-eval-agent)

帮开发者提效，开发过程中的测试让 AI 完成。

基于 AI 的智能 Web 应用测试和调试平台。它通过 MCP 协议集成到 IDE 中，使用 Claude 大语言模型驱动 browser-use 库自动执行浏览器操作，能够智能地导航网页、填写表单、点击按钮等，同时实时捕获控制台日志、网络请求和页面截图。

开发者可以通过可视化界面监控 AI 代理的执行过程，支持暂停/恢复/停止操作，并能生成详细的 UX 评估报告，包括发现的问题、交互流程分析和改进建议，从而让开发者从繁琐的手动测试中解放出来，专注于更重要的开发工作。

## 总

可以看到很多项目已经基于 brower-use 做 AI 自动化测试了，过去前端的 UI 测试确实是一个问题，基本依赖于手动操作，对于重构、跑 CASE 是一个很大的痛点。

未来可以持续探索 AI 的自动化测试，但卡点可能将会是 token 的花费，简单任务试了一下对于 claude 模型单次会有几毛钱（如果并行 agent 执行复杂任务花费将不可控），试了ollama 本地的模型效果会差很多，速度也比较慢。

未来「效果」和「花费」如何达到平衡需要不断探索。 [Introduction - Browser Use](https://link.zhihu.com/?target=https%3A//docs.browser-use.com/introduction) 未来「效果」和「花费」如何达到平衡需要不断探索。

还没有人送礼物，鼓励一下作者吧

编辑于 2025-10-24 08:31・上海[自动化测试](https://www.zhihu.com/topic/19574587)[AI](https://www.zhihu.com/topic/19588023)[Agent](https://www.zhihu.com/topic/28352669)[低至9.9元/月，即拥有 7x 24小时在线、随时响应的AI助手](https://click.aliyun.com/m/1000410524/?spu=biz%3D0%26ci%3D3681003%26si%3D6ca9aa3f-9609-4e74-bf91-e74cfcd1e086%26ts%3D1773940869%26zid%3D1629)

[

最多三步，即可拥有7x24小时在线、随时响应的AI...

](https://click.aliyun.com/m/1000410524/?spu=biz%3D0%26ci%3D3681003%26si%3D6ca9aa3f-9609-4e74-bf91-e74cfcd1e086%26ts%3D1773940869%26zid%3D1629)