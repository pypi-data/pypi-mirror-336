from bs4.element import Tag
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class UnifiedFinder:
    def find(self, element, selector=None, multiple=False):
        if selector is None:
            raise ValueError("Selector must be provided.")
        
        # 기본적으로 'tag'로 동작
        by = 'tag'

        if isinstance(element, Tag):
            return element.find_all(selector) if multiple else element.find(selector)
        
        elif isinstance(element, (WebDriver, WebElement)):
            by_map = {
                'tag': By.TAG_NAME,
                'class': By.CLASS_NAME,
                'id': By.ID,
                'css': By.CSS_SELECTOR
            }
            # 기본적으로 'tag'로 설정, selector가 class나 id로 들어오면 그에 맞는 셀렉터로
            if '.' in selector:
                by = 'class'
                selector = selector[1:]  # 'btn' → '.btn'일 때 class로 처리
            elif '#' in selector:
                by = 'id'
                selector = selector[1:]  # 'menu' → '#menu'일 때 id로 처리

            # Selenium에서 해당 요소 찾기
            return element.find_elements(by_map[by], selector) if multiple else element.find_element(by_map[by], selector)
        else:
            raise TypeError("Unsupported element type.")

    def finds(self, element, selector=None):
        return self.find(element, selector, multiple=True)

    def get_links(self, element, selector='a'):
        elements = self.find(element, selector, multiple=True)
        return [el.get('href') if isinstance(el, Tag) else el.get_attribute('href') for el in elements if el]

    def get_attr(self, element, selector, attr):
        tag = self.find(element, selector)
        return tag.get(attr) if isinstance(tag, Tag) else tag.get_attribute(attr) if tag else None

    def get_text(self, element, selector):
        tag = self.find(element, selector)
        return tag.text.strip() if tag else None

    def get_texts(self, element, selector):
        tags = self.find(element, selector, multiple=True)
        return [tag.text.strip() for tag in tags if tag]
    
    def get_elements_as_dict(self, element, selector, attrs):
        tags = self.find(element, selector, multiple=True)
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

    def exists(self, element, selector):
        try:
            return bool(self.find(element, selector))
        except:
            return False