from nose.tools import eq_

from ..detector import Detector

def test_detector():
	detector = Detector(2)
	
	eq_(list(detector.process([("a", {'id': 1})])), [])
	
	# Check noop
	eq_(list(detector.process([("a", {'id': 2})])), [])
	
	# Short revert
	eq_(list(detector.process([("b", {'id': 3})])), [])
	eq_(
		list(detector.process([("a", {'id': 4})])),
		[({'id': 4}, [{'id': 3}], {'id': 2})]
	)
	
	# Medium revert
	eq_(list(detector.process([("c", {'id': 4})])), [])
	eq_(list(detector.process([("d", {'id': 5})])), [])
	eq_(
		list(detector.process([("a", {'id': 6})])),
		[({'id': 6}, [{'id': 5}, {'id': 4}], {'id': 4})]
	)
	
	# Long (undetected) revert
	eq_(list(detector.process([("e", {'id': 7})])), [])
	eq_(list(detector.process([("f", {'id': 8})])), [])
	eq_(list(detector.process([("g", {'id': 9})])), [])
	eq_(
		list(detector.process([("a", {'id': 10})])),
		[]
	)
