from bs4.element import Tag
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class UnifiedFinder:
    def find(self, element, by, selector, multiple=False):
        if isinstance(element, Tag):
            if by == 'tag':
                return element.find_all(selector) if multiple else element.find(selector)
            elif by == 'class':
                return element.find_all(class_=selector) if multiple else element.find(class_=selector)
            elif by == 'id':
                return element.find_all(id=selector) if multiple else element.find(id=selector)
            elif by == 'attrs':
                return element.find_all(attrs=selector) if multiple else element.find(attrs=selector)
            else:
                raise ValueError("BeautifulSoup는 by='tag', 'class', 'id', 'attrs'만 지원합니다.")
        elif isinstance(element, (WebDriver, WebElement)):
            by_map = {
                'id': By.ID,
                'class': By.CLASS_NAME,
                'tag': By.TAG_NAME,
                'name': By.NAME,
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH
            }
            if by not in by_map:
                raise ValueError("Selenium은 by='id', 'class', 'tag', 'name', 'css', 'xpath'만 지원합니다.")
            return element.find_elements(by_map[by], selector) if multiple else element.find_element(by_map[by], selector)
        else:
            raise TypeError("지원되지 않는 element 타입입니다.")

    def get_links(self, element, by='tag', selector='a'):
        elements = self.find(element, by=by, selector=selector, multiple=True)
        return [el.get('href') if isinstance(el, Tag) else el.get_attribute('href') for el in elements if el]

    def get_link(self, element, by='tag', selector='a'):
        tag = self.find(element, by=by, selector=selector)
        return tag.get('href') if isinstance(tag, Tag) else tag.get_attribute('href') if tag else None

    def get_attr(self, element, by, selector, attr):
        tag = self.find(element, by=by, selector=selector)
        if tag:
            return tag.get(attr) if isinstance(tag, Tag) else tag.get_attribute(attr)
        return None

    def get_attrs(self, element, by, selector, attr):
        tags = self.find(element, by=by, selector=selector, multiple=True)
        return [tag.get(attr) if isinstance(tag, Tag) else tag.get_attribute(attr) for tag in tags if tag]

    def get_text(self, element, by, selector):
        tag = self.find(element, by=by, selector=selector)
        return tag.text.strip() if tag else None

    def get_texts(self, element, by, selector):
        tags = self.find(element, by=by, selector=selector, multiple=True)
        return [tag.text.strip() for tag in tags if tag]

    def get_elements_as_dict(self, element, by, selector, attrs):
        tags = self.find(element, by=by, selector=selector, multiple=True)
        results = []
        for tag in tags:
            result = {}
            for attr in attrs:
                if attr == 'text':
                    result['text'] = tag.text.strip()
                else:
                    result[attr] = tag.get(attr) if isinstance(tag, Tag) else tag.get_attribute(attr)
            results.append(result)
        return results

    def exists(self, element, by, selector):
        try:
            return bool(self.find(element, by, selector))
        except:
            return False