from typing import Dict, List

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import BaseScroll, WhenCondition, OnPageChangedVariants
from aiogram_dialog.widgets.text import Text


class ScrollingText(Text, BaseScroll):
    def __init__(
            self,
            text: Text,
            id: str,
            page_size: int = 0,
            when: WhenCondition = None,
            on_page_changed: OnPageChangedVariants = None,
    ):
        Text.__init__(self, when=when)
        BaseScroll.__init__(self, id=id, on_page_changed=on_page_changed)
        self.text = text
        self.page_size = page_size

    def _get_page_count(
            self,
            text: str,
    ) -> int:
        lines = text.split("\n")
        line_count = sum(1 for line in lines if len(line.strip()) > 0)
        return line_count // self.page_size + bool(line_count % self.page_size)

    async def _render_contents(
            self,
            data: Dict,
            manager: DialogManager,
    ) -> str:
        return await self.text.render_text(data, manager)

    @staticmethod
    def _split_text_by_lines(text: str) -> List[str]:
        lines = text.split("\n")
        return [line for line in lines if len(line.strip()) > 0]

    async def _render_text(self, data, manager: DialogManager) -> str:
        text = await self._render_contents(data, manager)
        lines = self._split_text_by_lines(text)
        page_count = self._get_page_count(text)
        page = await self.get_page(manager)
        last_page = page_count - 1
        current_page = min(last_page, page)
        line_offset = current_page * self.page_size
        line_limit = line_offset + self.page_size
        lines_to_render = lines[line_offset:line_limit]
        return "\n".join(lines_to_render)

    async def get_page_count(self, data: Dict, manager: DialogManager) -> int:
        text = await self._render_contents(data, manager)
        return self._get_page_count(text)
