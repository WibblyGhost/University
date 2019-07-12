"""
File: patient_queue.py
Author: Zachary Sanson

Maintain a patient queue that sorts patients based on the diseases
they have been diagnosed with, and the duration of time since the
diagnosis.
"""

from classes import PriorityQueue, Patient


class PatientHeapQueue(PriorityQueue):
    """ Implement a queue structure using a 0-indexed heap.
        This particular type of queue holds patient information.
    """

    def __init__(self, start_data=None, fast=False):
        """ Create the patient queue.
        """
        if start_data is None:
            start_data = []
        self.comparisons = 0
        self.data = []
        if fast:
            self._fast_heapify(start_data)
        else:
            self._heapify(start_data)

    def _swap(self, i, j):
        """ Swap the patients at positions i and j.
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _parent_index(self, index):
        """ Determine the parent index of the current index.
            For a binary heap that is zero-indexed, this is
            p = (i - 1) // 2
        """
        return (index - 1) // 2

    def _child_indices(self, index):
        """ Calculate the child indices for the current index.
            For a binary heap that is zero-indexed, this is
            c1 = 2*i + 1
            c2 = 2*i + 2
        """
        return [
            2 * index + delta
            for delta in range(1, 2 + 1)
        ]

    def _max_child_priority_index(self, child_indices):
        """ Find the child among the given indices that has the highest priority.
            If an index is not valid, do not consider it. If none are valid, then
            return None. Assumes the child_indices are in order.
        """
        max_index = None
        for index in child_indices:
            if index >= len(self.data):
                break  # No more valid children
            if max_index is None:  # This is the first child, it's valid, so use it
                max_index = index
            else:
                self.comparisons += 1  # Don't worry, we do the comparison counting here
                if self.data[index].priority > self.data[max_index].priority:
                    max_index = index
        return max_index

    def _sift_up(self, index):
        """ Move the patient at the given index into the correct location
            further up in the heap by swapping with its parents if appropriate.
        """
        # Recursive sifting, checks values are in the right place
        if index != 0 and index < len(self.data):
            self.comparisons += 1
            if self.data[index].priority > \
                    self.data[self._parent_index(index)].priority:
                self._swap(index, self._parent_index(index))
                self._sift_up(self._parent_index(index))

    def _sift_down(self, index):
        """ Move the patient at the given index into the correct location
            further down in the heap by swapping with its children if appropriate.
        """
        # Recursive sifting, checks values are in the right place.
        children = self._child_indices(index)
        max_child = self._max_child_priority_index(children)
        if max_child is not None:
            self.comparisons += 1
            if self.data[index].priority < self.data[max_child].priority:
                self._swap(index, max_child)
                self._sift_down(max_child)

    def _heapify(self, data):
        """ Turn the existing data into a heap in O(n log n) time.
        """
        for patient in data:
            self.enqueue(patient)

    def _fast_heapify(self, data):
        """ Turn the existing data into a heap in O(n) time.
        """
        for patient in data:
            assert isinstance(patient, Patient)
            self.data.append(patient)
        for index in range(len(self.data) - 1, -1, -1):
            self._sift_down(index)

    def enqueue(self, patient):
        """ Add a patient to the queue.
        """
        # We first make sure that we're only including Patients
        assert isinstance(patient, Patient)
        # Add patient to list and check for max heap
        self.data.append(patient)
        self._sift_up(len(self.data) - 1)

    def dequeue(self):
        """ Take a patient off the queue and return the Patient object
        """
        # Swap max and min values then remove the max value.
        if len(self.data) > 1:
            max_value = self.data[0]
            self.data[0] = self.data.pop()
            self._sift_down(0)
        else:
            max_value = self.data.pop()
        return max_value


class EditablePatientHeapQueue(PatientHeapQueue):
    """ Implement a queue structure using a 0-indexed heap.
        This particular type of queue holds patient information.
        Additionally, we can remove patients not at the top of
        the heap in O(log n) time.
    """

    def __init__(self, start_data=None, fast=False):
        self.indices = {}  # name -> index;
                          # Keep track of where patients are stored
        for (i, person) in enumerate(start_data):
            self.indices[person.name] = i
        super().__init__(start_data, fast)

    def _swap(self, i, j):
        """ Swap patients at index i and j. Don't forget to change
            their position in self.indices as well!
        """
        # Change indices value then swap
        self.indices[self.data[i].name], self.indices[self.data[j].name] = j, i
        super()._swap(i, j)

    def remove(self, patient_name):
        """ Remove the particular patient from the heap. Remember,
            the index will tell you where the patient is in the heap
            and every sub-heap below an index forms a valid heap.
        """
        if len(self.data) < 2:
            self.indices.clear()
            self.data.pop()
        else:
            # Indexes
            curr_index, min_index = self.indices[patient_name], \
                                    len(self.data) - 1
            # Swap positions, min & index
            self.indices[patient_name], self.indices[self.data[-1].name] = \
                self.indices[self.data[-1].name], self.indices[patient_name]
            self.data[curr_index], self.data[min_index] = \
                self.data[min_index], self.data[curr_index]
            # Delete at index (new min)
            self.data.pop()
            del self.indices[patient_name]
            # Sift heap
            super()._sift_up(curr_index)
            super()._sift_down(curr_index)

    def enqueue(self, patient):
        """ Add a patient to the queue. Let the superclass do
            most of the work.
        """
        # Enqueue:  ## enqueue -> _sift_up -> _swap
        self.indices[patient.name] = len(self.data)
        super().enqueue(patient)

    def dequeue(self):
        """ Remove a patient from the front of the queue and return them.
            Again, let the superclass do most of the work.
        """
        # Dequeue:  ## dequeue -> _sift_down -> _swap
        result, value = self.data[0], self.indices[self.data[0].name]
        del self.indices[self.data[0].name]
        self.indices[self.data[-1].name] = value
        super().dequeue()
        if len(self.data) < 1:
            self.indices.clear()
        return result
