// int_queue.cpp  (P1)
// Cola circular sobre arreglo fijo. head_ = índice del frente, count_ = elementos.
#include "kahn_interface.hpp"
#include <stdexcept>

IntQueue::IntQueue(int capacity)
    : buf_(capacity > 0 ? capacity : 1), head_(0), count_(0) {}

void IntQueue::push(int x) {
    int cap = static_cast<int>(buf_.size());
    if (count_ == cap) throw std::overflow_error("IntQueue llena");
    buf_[(head_ + count_) % cap] = x;
    ++count_;
}

int IntQueue::pop() {
    if (count_ == 0) throw std::underflow_error("IntQueue vacia");
    int x = buf_[head_];
    head_ = (head_ + 1) % static_cast<int>(buf_.size());
    --count_;
    return x;
}

int IntQueue::front() const {
    if (count_ == 0) throw std::underflow_error("IntQueue vacia");
    return buf_[head_];
}

bool IntQueue::empty() const { return count_ == 0; }

int IntQueue::size() const { return count_; }

// frente -> fondo (lo usa la traza para dibujar la cola)
std::vector<int> IntQueue::snapshot() const {
    std::vector<int> s;
    s.reserve(count_);
    int cap = static_cast<int>(buf_.size());
    for (int i = 0; i < count_; ++i)
        s.push_back(buf_[(head_ + i) % cap]);
    return s;
}
