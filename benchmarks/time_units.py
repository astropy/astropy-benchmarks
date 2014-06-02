from astropy import units as u
import copy


def time_unit_compose():
    u.Ry.compose()


def time_unit_to():
    u.m.to(u.pc)


def time_unit_parse():
    u.Unit('1e-07 kg m2 / s2')


def time_simple_unit_parse():
    u.Unit('1 d')


def time_very_simple_unit_parse():
    u.Unit('d')


def mem_unit():
    return u.erg


def time_compose_to_bases():
    x = copy.copy(u.Ry)
    x.cgs
