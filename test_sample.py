# -*- coding: utf-8 -*-

def test_conftest_01(driver, cfg):
    for k, v in cfg.items(): # output the cfg dict key value pairs individually
        print("cfg key: {0} -> value: {1}".format(k, v))
    driver.get(cfg['base_url']) # navigate to specified url
    cfg['blah'] = 'bumblebeetuna' # add a key to cfg dict
    for k, v in cfg.items(): # output the cfg dict key value pairs individually
        print("cfg key: {0} -> value: {1}".format(k, v))
    assert False # to show output in terminal

def test_conftest_02(driver, cfg):
    for k, v in cfg.items(): # output the cfg dict key value pairs individually,
                             # cfg['blah'] key should not be present in output for this test
        print("cfg key: {0} -> value: {1}".format(k, v))
    driver.get(cfg['base_url']) # navigate to specified url
    assert False # to show output in terminal
