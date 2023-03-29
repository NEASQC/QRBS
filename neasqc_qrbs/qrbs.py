# -*- coding : utf-8 -*

from abc import ABC, abstractmethod

from .knowledge_rep import Fact, Rule, KnowledgeIsland


class WorkingMemory():
    """Class representing a Working Memory. 
    
    A Working Memory is an element of a Rule-Based System that manages its facts, keeping trace of their state.

    Attributes:
        _facts (List[:obj:`Fact`], optional): List of facts asserted into the system.
    """

    def __init__(self, facts=[]) -> None:
        super().__init__()
        self._facts = []
        for fact in facts:
            self.assert_fact(fact)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._facts == other._facts

    def assert_fact(self, fact) -> Fact:
        """Asserts a fact into the memory.

        Args:
            fact (:obj:`Fact`): The fact to be asserted.

        Returns:
            :obj:`Fact`: The asserted fact.
        """
        self._facts.append(fact)
        return fact

    def retract_fact(self, fact) -> None:
        """Retracts a fact from the memory.

        Args:
            fact (:obj:`Fact`): The fact to be retracted.
        """
        self._facts.remove(fact)


class InferenceEngine():
    """Class representing an Inference Engine. 
    
    An Inference Engine is an element of a Rule-Based System that manages its rules and knowledge islands, providing the tools to evaluate them in order.

    Attributes:
        _rules (List[:obj:`Rule`], optional): List of rules established for the system.
        _islands (List[:obj:`KnowledgeIsland`], optional): List of knowledge island established for the system.
    """

    def __init__(self, rules=[], islands=[]) -> None:
        super().__init__()
        self._rules = []
        for rule in rules:
            self.assert_rule(rule)
        self._islands = []
        for island in islands:
            self.assert_island(island)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._rules == other._rules and self._islands == other._islands

    def assert_rule(self, rule) -> Rule:
        """Asserts a rule into the engine.

        Args:
            rule (:obj:`Rule`): The rule to be asserted.

        Returns:
            :obj:`Rule`: The asserted rule.
        """
        self._rules.append(rule)
        return rule

    def retract_rule(self, rule) -> None:
        """Retracts a rule from the engine.

        Args:
            rule (:obj:`Rule`): The rule to be retracted.

        Raises:
            AttributeError: In case the rule to be retracted is part of a knowledge island.
        """
        for island in self._islands:
            if rule in island.rules:
                raise AttributeError('The rule to be retracted is part of a knowledge island and cannot be retracted')
        self._rules.remove(rule)

    def assert_island(self, island) -> KnowledgeIsland:
        """Asserts a knowledge island into the engine.

        Args:
            island (:obj:`KnowledgeIsland`): The knowledge island to be asserted.

        Returns:
            :obj:`KnowledgeIsland`: The asserted knowledge island.

        Raises:
            AttributeError: In case the rules that compose the knowledge island are not asserted in the system's inference engine or \
            the rules that compose the knowledge island are not chained.
        """
        def find_link(chain, rules):
            found_link = None
            for link in chain:
                for rule in rules:
                    if (link.righthandside in rule.lefthandside) or (rule.righthandside in link.lefthandside) and (rule not in chain):
                        found_link = rule
                        chain.append(found_link)
                        break
            return found_link

        if [rule for rule in island.rules if rule in self._rules] != island.rules:
            raise AttributeError('The rules of the knowledge island are not asserted in the system')
        
        chain = island.rules[:1]
        link = chain[0]
        while link != None and [rule for rule in island.rules if rule in chain] != island.rules:
            link = find_link(chain, island.rules)
        if link == None:
            raise AttributeError('The rules of the knowledge island are not chained')
        
        self._islands.append(island)
        return island

    def retract_island(self, island) -> None:
        """Retracts a knowledge island from the engine.

        Args:
            island (:obj:`KnowledgeIsland`): The knowledge island to be retracted.
        """
        self._islands.remove(island)


class QRBS():
    """Class representing a Quantum Rule-Based System. 
    
    A Quantum Rule-Based System (QRBS) is a Rule-Based System implemented in a quantum computer, taking advatange of some of its capabilities, like quantum superposition, to represent certain aspects such as imprecission and uncertainty.

    Attributes:
        _memory (:obj:`WorkingMemory`): The Working Memory of the system.
        _engine (:obj:`InferenceEngine`): The Inference Engine of the system.
    """

    def __init__(self) -> None:
        super().__init__()
        self._memory = WorkingMemory()
        self._engine = InferenceEngine()

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._memory == other._memory and self._engine == other._engine

    def assert_fact(self, attribute, value, imprecission=0.0) -> Fact:
        """Creates a fact and asserts it into the system.

        Args:
            attribute (str): The attribute of the fact.
            value (float): The value of the fact.
            imprecission (float, optional): The imprecission of the rule.

        Returns:
            :obj:`Rule`: The asserted rule.
        """
        fact = Fact(attribute, value, imprecission)
        return self._memory.assert_fact(fact)

    def retract_fact(self, fact) -> None:
        """Retracts a fact from the system.

        Args:
            fact (:obj:`Fact`): The fact to be retracted.
        """
        for rule in self._engine._rules:
            if fact in rule.lefthandside or fact in rule.righthandside:
                raise AttributeError('The fact to be retracted is part of a rule and cannot be retracted')
        self._memory.retract_fact(fact)

    def assert_rule(self, lefthandside, righthandside, uncertainty=0.0) -> Rule:
        """Creates a rule and asserts it into the system.

        Args:
            lefthandside (:obj:`LeftHandSide`): The left hand side of the rule.
            righthandside (:obj:`Fact`): The right hand side of the rule.
            uncertainty (float, optional): The uncertainty of the rule.

        Returns:
            :obj:`Rule`: The asserted rule.
        """
        rule = Rule(lefthandside, righthandside, uncertainty)
        return self._engine.assert_rule(rule)

    def retract_rule(self, rule) -> None:
        """Retracts a rule from the system.

        Args:
            rule (:obj:`Rule`): The rule to be retracted.
        """
        self._engine.retract_rule(rule)

    def assert_island(self, rules) -> KnowledgeIsland:
        """Creates a knowledge island and asserts it into the system.

        Args:
            rules (List[:obj:`Rule`]): The rules of the knowledge island.

        Returns:
            :obj:`KnowledgeIsland`: The asserted knowledge island.
        """
        island = KnowledgeIsland(rules)
        return self._engine.assert_island(island)

    def retract_island(self, island) -> None:
        """Retracts a knowledge island from the system.

        Args:
            island (:obj:`KnowledgeIsland`): The knowledge island to be retracted.
        """
        self._engine.retract_island(island)
        

class QRBSHandler():
    """Class encapsulating QRBS handling methods. 
    
    This class proporcionates several methods to handle operations related to Quantum Rule-Based Systems, such as their evaluation or execution.
    """

    @staticmethod
    def evaluate(qrbs, qpu) -> None:
        """Evaluates whether a QRBS can be executed on a QPU.

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be evaluated.
            qpu (:obj:`QPU`): The QPU in which the QRBS must be evaluated.
        """
        pass

    @staticmethod
    def execute(qrbs, qpu) -> None:
        """Executes the QRBS on the QPU.

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be executed.
            qpu (:obj:`QPU`): The QPU in which the QRBS must be executed.
        """
        pass
      

class QPU(ABC):
    """Interface defining the structure to implement Quantum Processing Units (QPU).
    """

    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def evaluate(circuit) -> None:
        """Evaluates whether a quantum circuit can be executed on this QPU.

        Args:
            circuit (:obj:`Circuit`): The circuit to be evaluated.
        """
        pass

    @abstractmethod
    def execute(circuit) -> None:
        """Executes the circuit on this QPU.

        Args:
            circuit (:obj:`Circuit`): The circuit to be executed.
        """
        pass
      

class MyQlmQPU(QPU):
    """ myQLM implementation of a Quantum Processing Unit (QPU).
    """

    def __init__(self) -> None:
        super().__init__()
        
    def evaluate(circuit) -> None:
        """Evaluates whether a quantum circuit can be executed on this QPU.

        Args:
            circuit (:obj:`Circuit`): The circuit to be evaluated.
        """
        pass

    def execute(circuit) -> None:
        """Executes the circuit on this QPU.

        Args:
            circuit (:obj:`Circuit`): The circuit to be executed.
        """
        pass