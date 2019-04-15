# -*- coding: utf-8 -*-

import pytest
from base import Base

class TestBaseNav():

    @pytest.fixture
    def base_util(self, driver):
        return Base(driver)
        
    @pytest.mark.smoke
    def test_base_nav(self, base_util):
        base_util.navigate_to("/blah")
