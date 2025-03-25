/* 
 * Matrix.hpp 
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

/**
 * \file
 * \brief Definition of matrix data types.
 */

#ifndef CDPL_MATH_MATRIX_HPP
#define CDPL_MATH_MATRIX_HPP

#include <cstddef>
#include <cstdint>
#include <algorithm>
#include <vector>
#include <limits>
#include <unordered_map>
#include <type_traits>
#include <utility>
#include <initializer_list>
#include <memory>

#include "CDPL/Math/Check.hpp"
#include "CDPL/Math/MatrixExpression.hpp"
#include "CDPL/Math/MatrixAssignment.hpp"
#include "CDPL/Math/DirectAssignmentProxy.hpp"
#include "CDPL/Math/Functional.hpp"
#include "CDPL/Math/TypeTraits.hpp"
#include "CDPL/Math/SparseContainerElement.hpp"
#include "CDPL/Math/LUDecomposition.hpp"
#include "CDPL/Base/Exceptions.hpp"


namespace CDPL
{

    namespace Math
    {

        template <typename M>
        class MatrixReference : public MatrixExpression<MatrixReference<M> >
        {

            typedef MatrixReference<M> SelfType;

          public:
            typedef M                                                      MatrixType;
            typedef typename M::ValueType                                  ValueType;
            typedef typename std::conditional<std::is_const<M>::value,
                                              typename M::ConstReference,
                                              typename M::Reference>::type Reference;
            typedef typename M::ConstReference                             ConstReference;
            typedef typename M::SizeType                                   SizeType;
            typedef typename M::DifferenceType                             DifferenceType;
            typedef SelfType                                               ClosureType;
            typedef const SelfType                                         ConstClosureType;

            explicit MatrixReference(MatrixType& m):
                data(m) {}

            Reference operator()(SizeType i, SizeType j)
            {
                return data(i, j);
            }

            ConstReference operator()(SizeType i, SizeType j) const
            {
                return data(i, j);
            }

            SizeType getSize1() const
            {
                return data.getSize1();
            }

            SizeType getSize2() const
            {
                return data.getSize2();
            }

            SizeType getMaxSize() const
            {
                return data.getMaxSize();
            }

            SizeType getMaxSize1() const
            {
                return data.getMaxSize1();
            }

            SizeType getMaxSize2() const
            {
                return data.getMaxSize2();
            }

            bool isEmpty() const
            {
                return data.isEmpty();
            }

            const MatrixType& getData() const
            {
                return data;
            }

            MatrixType& getData()
            {
                return data;
            }

            MatrixReference& operator=(const MatrixReference& r)
            {
                data.operator=(r.data);
                return *this;
            }

            template <typename E>
            MatrixReference& operator=(const MatrixExpression<E>& e)
            {
                data.operator=(e);
                return *this;
            }

            template <typename E>
            MatrixReference& operator+=(const MatrixExpression<E>& e)
            {
                data.operator+=(e);
                return *this;
            }

            template <typename E>
            MatrixReference& operator-=(const MatrixExpression<E>& e)
            {
                data.operator-=(e);
                return *this;
            }

            template <typename T>
            typename std::enable_if<IsScalar<T>::value, MatrixReference>::type& operator*=(const T& t)
            {
                data.operator*=(t);
                return *this;
            }

            template <typename T>
            typename std::enable_if<IsScalar<T>::value, MatrixReference>::type& operator/=(const T& t)
            {
                data.operator/=(t);
                return *this;
            }

            template <typename E>
            MatrixReference& assign(const MatrixExpression<E>& e)
            {
                data.assign(e);
                return *this;
            }

            template <typename E>
            MatrixReference& plusAssign(const MatrixExpression<E>& e)
            {
                data.plusAssign(e);
                return *this;
            }

            template <typename E>
            MatrixReference& minusAssign(const MatrixExpression<E>& e)
            {
                data.minusAssign(e);
                return *this;
            }

            void swap(MatrixReference& r)
            {
                data.swap(r.data);
            }

            friend void swap(MatrixReference& r1, MatrixReference& r2)
            {
                r1.swap(r2);
            }

          private:
            MatrixType& data;
        };

        template <typename T, typename A>
        class Matrix;
        template <typename T, typename A>
        class Vector;

        template <typename T>
        class InitListMatrix : public MatrixContainer<InitListMatrix<T> >
        {

          public:
            typedef InitListMatrix                                            SelfType;
            typedef std::initializer_list<std::initializer_list<T> >          InitializerListType;
            typedef typename InitializerListType::value_type::value_type      ValueType;
            typedef typename InitializerListType::value_type::const_reference ConstReference;
            typedef typename InitializerListType::value_type::reference       Reference;
            typedef typename InitializerListType::size_type                   SizeType;
            typedef typename std::ptrdiff_t                                   DifferenceType;
            typedef SelfType                                                  ClosureType;
            typedef const SelfType                                            ConstClosureType;
            typedef Matrix<T, std::vector<T> >                                MatrixTemporaryType;
            typedef Vector<T, std::vector<T> >                                VectorTemporaryType;

            InitListMatrix(InitializerListType l):
                list(l), size2(0)
            {
                for (const auto& r : l)
                    size2 = std::max(size2, r.size());
            }

            Reference operator()(SizeType i, SizeType j)
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);

                if (j >= (list.begin() + i)->size())
                    return zero;

                return *((list.begin() + i)->begin() + j);
            }

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);

                if (j >= (list.begin() + i)->size())
                    return zero;

                return *((list.begin() + i)->begin() + j);
            }

            SizeType getSize1() const
            {
                return list.size();
            }

            SizeType getSize2() const
            {
                return size2;
            }

            bool isEmpty() const
            {
                return (size2 == 0 || list.size() == 0);
            }

          private:
            InitializerListType    list;
            SizeType               size2;
            static const ValueType zero;
        };

        template <typename T>
        const typename InitListMatrix<T>::ValueType InitListMatrix<T>::zero = InitListMatrix<T>::ValueType();

        template <typename T, typename A = std::vector<T> >
        class Matrix : public MatrixContainer<Matrix<T, A> >
        {

            typedef Matrix<T, A> SelfType;

          public:
            typedef T                                                ValueType;
            typedef T&                                               Reference;
            typedef const T&                                         ConstReference;
            typedef typename A::size_type                            SizeType;
            typedef typename A::difference_type                      DifferenceType;
            typedef A                                                ArrayType;
            typedef T*                                               Pointer;
            typedef const T*                                         ConstPointer;
            typedef MatrixReference<SelfType>                        ClosureType;
            typedef const MatrixReference<const SelfType>            ConstClosureType;
            typedef SelfType                                         MatrixTemporaryType;
            typedef Vector<T, A>                                     VectorTemporaryType;
            typedef std::shared_ptr<SelfType>                        SharedPointer;
            typedef std::initializer_list<std::initializer_list<T> > InitializerListType;

            Matrix():
                size1(0), size2(0), data() {}

            Matrix(SizeType m, SizeType n):
                size1(m), size2(n), data(storageSize(m, n)) {}

            Matrix(SizeType m, SizeType n, const ValueType& v):
                size1(m), size2(n), data(storageSize(m, n), v) {}

            Matrix(const Matrix& m):
                size1(m.size1), size2(m.size2), data(m.data) {}

            Matrix(Matrix&& m):
                size1(0), size2(0), data()
            {
                swap(m);
            }

            Matrix(InitializerListType l):
                size1(0), size2(0), data()
            {
                assign(l);
            }

            template <typename E>
            Matrix(const MatrixExpression<E>& e):
                size1(e().getSize1()), size2(e().getSize2()), data(storageSize(e().getSize1(), e().getSize2()))
            {
                matrixAssignMatrix<ScalarAssignment>(*this, e);
            }

            Reference operator()(SizeType i, SizeType j)
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return data[i * getSize2() + j];
            }

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return data[i * getSize2() + j];
            }

            bool isEmpty() const
            {
                return data.empty();
            }

            SizeType getSize1() const
            {
                return size1;
            }

            SizeType getSize2() const
            {
                return size2;
            }

            SizeType getMaxSize() const
            {
                return data.max_size();
            }

            ArrayType& getData()
            {
                return data;
            }

            const ArrayType& getData() const
            {
                return data;
            }

            Matrix& operator=(const Matrix& m)
            {
                data  = m.data;
                size1 = m.size1;
                size2 = m.size2;
                return *this;
            }

            Matrix& operator=(Matrix&& m)
            {
                swap(m);
                return *this;
            }

            template <typename C>
            Matrix& operator=(const MatrixContainer<C>& c)
            {
                return assign(c);
            }

            Matrix& operator=(InitializerListType l)
            {
                return assign(l);
            }

            template <typename E>
            Matrix& operator=(const MatrixExpression<E>& e)
            {
                Matrix tmp(e);
                swap(tmp);
                return *this;
            }

            template <typename C>
            Matrix& operator+=(const MatrixContainer<C>& c)
            {
                return plusAssign(c);
            }

            Matrix& operator+=(InitializerListType l)
            {
                return plusAssign(l);
            }

            template <typename E>
            Matrix& operator+=(const MatrixExpression<E>& e)
            {
                Matrix tmp(*this + e);
                swap(tmp);
                return *this;
            }

            template <typename C>
            Matrix& operator-=(const MatrixContainer<C>& c)
            {
                return minusAssign(c);
            }

            Matrix& operator-=(InitializerListType l)
            {
                return minusAssign(l);
            }

            template <typename E>
            Matrix& operator-=(const MatrixExpression<E>& e)
            {
                Matrix tmp(*this - e);
                swap(tmp);
                return *this;
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, Matrix>::type& operator*=(const T1& t)
            {
                matrixAssignScalar<ScalarMultiplicationAssignment>(*this, t);
                return *this;
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, Matrix>::type& operator/=(const T1& t)
            {
                matrixAssignScalar<ScalarDivisionAssignment>(*this, t);
                return *this;
            }

            template <typename E>
            Matrix& assign(const MatrixExpression<E>& e)
            {
                resize(e().getSize1(), e().getSize2(), false);
                matrixAssignMatrix<ScalarAssignment>(*this, e);
                return *this;
            }

            Matrix& assign(InitializerListType l)
            {
                InitListMatrix<ValueType> ilm(l);
                resize(ilm.getSize1(), ilm.getSize2(), false);
                matrixAssignMatrix<ScalarAssignment>(*this, ilm);
                return *this;
            }

            template <typename E>
            Matrix& plusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, e);
                return *this;
            }

            Matrix& plusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            template <typename E>
            Matrix& minusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, e);
                return *this;
            }

            Matrix& minusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            void swap(Matrix& m)
            {
                if (this != &m) {
                    std::swap(data, m.data);
                    std::swap(size1, m.size1);
                    std::swap(size2, m.size2);
                }
            }

            friend void swap(Matrix& m1, Matrix& m2)
            {
                m1.swap(m2);
            }

            void clear(const ValueType& v = ValueType())
            {
                std::fill(data.begin(), data.end(), v);
            }

            void resize(SizeType m, SizeType n, bool preserve = true, const ValueType& v = ValueType())
            {
                if (size1 == m && size2 == n)
                    return;

                if (preserve) {
                    Matrix tmp(m, n, v);

                    for (SizeType i = 0, min_size1 = std::min(size1, m); i < min_size1; i++)
                        for (SizeType j = 0, min_size2 = std::min(size2, n); j < min_size2; j++)
                            tmp(i, j) = (*this)(i, j);

                    swap(tmp);

                } else {
                    data.resize(storageSize(m, n), v);
                    size1 = m;
                    size2 = n;
                }
            }

          private:
            SizeType storageSize(SizeType m, SizeType n)
            {
                CDPL_MATH_CHECK(n == 0 || m <= data.max_size() / n, "Maximum size exceeded", Base::SizeError);
                return (m * n);
            }

            SizeType  size1;
            SizeType  size2;
            ArrayType data;
        };

        template <typename T, typename A = std::unordered_map<std::uint64_t, T> >
        class SparseMatrix : public MatrixContainer<SparseMatrix<T, A> >
        {

            typedef SparseMatrix<T> SelfType;

          public:
            typedef T                                                ValueType;
            typedef typename A::key_type                             KeyType;
            typedef SparseContainerElement<SelfType>                 Reference;
            typedef const T&                                         ConstReference;
            typedef std::uint32_t                                    SizeType;
            typedef std::ptrdiff_t                                   DifferenceType;
            typedef A                                                ArrayType;
            typedef T*                                               Pointer;
            typedef const T*                                         ConstPointer;
            typedef MatrixReference<SelfType>                        ClosureType;
            typedef const MatrixReference<const SelfType>            ConstClosureType;
            typedef SelfType                                         MatrixTemporaryType;
            typedef Vector<T, std::vector<T> >                       VectorTemporaryType;
            typedef std::shared_ptr<SelfType>                        SharedPointer;
            typedef std::initializer_list<std::initializer_list<T> > InitializerListType;

            SparseMatrix():
                size1(0), size2(0), data() {}

            SparseMatrix(SizeType m, SizeType n):
                size1(m), size2(n), data()
            {
                CDPL_MATH_CHECK((n == 0 || m <= data.max_size() / n), "Maximum size exceeded", Base::SizeError);
            }

            SparseMatrix(const SparseMatrix& m):
                size1(m.size1), size2(m.size2), data(m.data) {}

            SparseMatrix(SparseMatrix&& m):
                size1(0), size2(0), data()
            {
                swap(m);
            }

            SparseMatrix(InitializerListType l):
                size1(0), size2(0), data()
            {
                assign(l);
            }

            template <typename E>
            SparseMatrix(const MatrixExpression<E>& e):
                size1(e().getSize1()), size2(e().getSize2()), data()
            {
                CDPL_MATH_CHECK((size1 == 0 || size2 <= data.max_size() / size1), "Maximum size exceeded", Base::SizeError);
                matrixAssignMatrix<ScalarAssignment>(*this, e);
            }

            Reference operator()(SizeType i, SizeType j)
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);

                return Reference(*this, makeKey(i, j));
            }

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);

                typename ArrayType::const_iterator it = data.find(makeKey(i, j));

                if (it == data.end())
                    return zero;

                return it->second;
            }

            SizeType getNumElements() const
            {
                return data.size();
            }

            bool isEmpty() const
            {
                return (size1 == 0 || size2 == 0);
            }

            SizeType getSize1() const
            {
                return size1;
            }

            SizeType getSize2() const
            {
                return size2;
            }

            typename ArrayType::size_type getMaxSize() const
            {
                return data.max_size();
            }

            ArrayType& getData()
            {
                return data;
            }

            const ArrayType& getData() const
            {
                return data;
            }

            SparseMatrix& operator=(const SparseMatrix& m)
            {
                data  = m.data;
                size1 = m.size1;
                size2 = m.size2;
                return *this;
            }

            SparseMatrix& operator=(SparseMatrix&& m)
            {
                swap(m);
                return *this;
            }

            template <typename C>
            SparseMatrix& operator=(const MatrixContainer<C>& c)
            {
                return assign(c);
            }

            SparseMatrix& operator=(InitializerListType l)
            {
                return assign(l);
            }

            template <typename E>
            SparseMatrix& operator=(const MatrixExpression<E>& e)
            {
                SparseMatrix tmp(e);
                swap(tmp);
                return *this;
            }

            template <typename C>
            SparseMatrix& operator+=(const MatrixContainer<C>& c)
            {
                return plusAssign(c);
            }

            SparseMatrix& operator+=(InitializerListType l)
            {
                return plusAssign(l);
            }

            template <typename E>
            SparseMatrix& operator+=(const MatrixExpression<E>& e)
            {
                SparseMatrix tmp(*this + e);
                swap(tmp);
                return *this;
            }

            template <typename C>
            SparseMatrix& operator-=(const MatrixContainer<C>& c)
            {
                return minusAssign(c);
            }

            SparseMatrix& operator-=(InitializerListType l)
            {
                return minusAssign(l);
            }

            template <typename E>
            SparseMatrix& operator-=(const MatrixExpression<E>& e)
            {
                SparseMatrix tmp(*this - e);
                swap(tmp);
                return *this;
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, SparseMatrix>::type& operator*=(const T1& t)
            {
                matrixAssignScalar<ScalarMultiplicationAssignment>(*this, t);
                return *this;
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, SparseMatrix>::type& operator/=(const T1& t)
            {
                matrixAssignScalar<ScalarDivisionAssignment>(*this, t);
                return *this;
            }

            template <typename E>
            SparseMatrix& assign(const MatrixExpression<E>& e)
            {
                resize(e().getSize1(), e().getSize2());
                matrixAssignMatrix<ScalarAssignment>(*this, e);
                return *this;
            }

            SparseMatrix& assign(InitializerListType l)
            {
                InitListMatrix<ValueType> ilm(l);
                resize(ilm.getSize1(), ilm.getSize2());
                matrixAssignMatrix<ScalarAssignment>(*this, ilm);
                return *this;
            }

            template <typename E>
            SparseMatrix& plusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, e);
                return *this;
            }

            SparseMatrix& plusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            template <typename E>
            SparseMatrix& minusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, e);
                return *this;
            }

            SparseMatrix& minusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            void swap(SparseMatrix& m)
            {
                if (this != &m) {
                    std::swap(data, m.data);
                    std::swap(size1, m.size1);
                    std::swap(size2, m.size2);
                }
            }

            friend void swap(SparseMatrix& m1, SparseMatrix& m2)
            {
                m1.swap(m2);
            }

            void clear()
            {
                data.clear();
            }

            void resize(SizeType m, SizeType n)
            {
                CDPL_MATH_CHECK((n == 0 || m <= data.max_size() / n), "Maximum size exceeded", Base::SizeError);

                for (typename ArrayType::iterator it = data.begin(); it != data.end();) {
                    const KeyType& key = it->first;

                    if (getRowIdx(key) >= m || getColIdx(key) >= n)
                        it = data.erase(it);
                    else
                        ++it;
                }

                size1 = m;
                size2 = n;
            }

          private:
            static KeyType makeKey(SizeType i, SizeType j)
            {
                return ((KeyType(i) << (sizeof(SizeType) * 8)) + j);
            }

            static SizeType getRowIdx(const KeyType& key)
            {
                return (key >> (sizeof(SizeType) * 8));
            }

            static SizeType getColIdx(const KeyType& key)
            {
                return (key & KeyType(~SizeType()));
            }

            SizeType               size1;
            SizeType               size2;
            ArrayType              data;
            static const ValueType zero;
        };

        template <typename T, typename A>
        const typename SparseMatrix<T, A>::ValueType SparseMatrix<T, A>::zero = SparseMatrix<T, A>::ValueType();

        template <typename T, std::size_t N>
        class BoundedVector;

        template <typename T, std::size_t M, std::size_t N>
        class BoundedMatrix : public MatrixContainer<BoundedMatrix<T, M, N> >
        {

            typedef BoundedMatrix<T, M, N> SelfType;

          public:
            typedef T              ValueType;
            typedef T&             Reference;
            typedef const T&       ConstReference;
            typedef std::size_t    SizeType;
            typedef std::ptrdiff_t DifferenceType;
            typedef ValueType      ArrayType[M][N];
            typedef T (*ArrayPointer)[N];
            typedef const T (*ConstArrayPointer)[N];
            typedef T*                                               Pointer;
            typedef const T*                                         ConstPointer;
            typedef MatrixReference<SelfType>                        ClosureType;
            typedef const MatrixReference<const SelfType>            ConstClosureType;
            typedef SelfType                                         MatrixTemporaryType;
            typedef BoundedVector<T, M * N>                          VectorTemporaryType;
            typedef std::shared_ptr<SelfType>                        SharedPointer;
            typedef std::initializer_list<std::initializer_list<T> > InitializerListType;

            static const SizeType MaxSize1 = M;
            static const SizeType MaxSize2 = N;

            BoundedMatrix():
                size1(0), size2(0) {}

            BoundedMatrix(SizeType m, SizeType n):
                size1(0), size2(0)
            {
                resize(m, n);
            }

            BoundedMatrix(SizeType m, SizeType n, const ValueType& v):
                size1(0), size2(0)
            {
                resize(m, n, v);
            }

            BoundedMatrix(const BoundedMatrix& m):
                size1(m.size1), size2(m.size2)
            {
                for (SizeType i = 0; i < size1; i++)
                    std::copy(m.data[i], m.data[i] + size2, data[i]);
            }

            BoundedMatrix(InitializerListType l):
                size1(0), size2(0)
            {
                assign(l);
            }

            template <typename E>
            BoundedMatrix(const MatrixExpression<E>& e):
                size1(0), size2(0)
            {
                resize(e().getSize1(), e().getSize2());
                matrixAssignMatrix<ScalarAssignment>(*this, e);
            }

            Reference operator()(SizeType i, SizeType j)
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return data[i][j];
            }

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return data[i][j];
            }

            bool isEmpty() const
            {
                return (size1 == 0 || size2 == 0);
            }

            SizeType getSize1() const
            {
                return size1;
            }

            SizeType getSize2() const
            {
                return size2;
            }

            SizeType getMaxSize1() const
            {
                return M;
            }

            SizeType getMaxSize2() const
            {
                return N;
            }

            ArrayPointer getData()
            {
                return data;
            }

            ConstArrayPointer getData() const
            {
                return data;
            }

            BoundedMatrix& operator=(const BoundedMatrix& m)
            {
                if (this != &m) {
                    for (SizeType i = 0; i < m.size1; i++)
                        std::copy(m.data[i], m.data[i] + m.size2, data[i]);

                    size1 = m.size1;
                    size2 = m.size2;
                }

                return *this;
            }

            template <typename C>
            BoundedMatrix& operator=(const MatrixContainer<C>& c)
            {
                return assign(c);
            }

            BoundedMatrix& operator=(InitializerListType l)
            {
                return assign(l);
            }

            template <typename E>
            BoundedMatrix& operator=(const MatrixExpression<E>& e)
            {
                BoundedMatrix tmp(e);
                return this-> operator=(tmp);
            }

            template <typename C>
            BoundedMatrix& operator+=(const MatrixContainer<C>& c)
            {
                return plusAssign(c);
            }

            BoundedMatrix& operator+=(InitializerListType l)
            {
                return plusAssign(l);
            }

            template <typename E>
            BoundedMatrix& operator+=(const MatrixExpression<E>& e)
            {
                BoundedMatrix tmp(*this + e);
                return this-> operator=(tmp);
            }

            template <typename C>
            BoundedMatrix& operator-=(const MatrixContainer<C>& c)
            {
                return minusAssign(c);
            }

            BoundedMatrix& operator-=(InitializerListType l)
            {
                return minusAssign(l);
            }

            template <typename E>
            BoundedMatrix& operator-=(const MatrixExpression<E>& e)
            {
                BoundedMatrix tmp(*this - e);
                return this-> operator=(tmp);
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, BoundedMatrix>::type& operator*=(const T1& v)
            {
                matrixAssignScalar<ScalarMultiplicationAssignment>(*this, v);
                return *this;
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, BoundedMatrix>::type& operator/=(const T1& v)
            {
                matrixAssignScalar<ScalarDivisionAssignment>(*this, v);
                return *this;
            }

            template <typename E>
            BoundedMatrix& assign(const MatrixExpression<E>& e)
            {
                resize(e().getSize1(), e().getSize2());
                matrixAssignMatrix<ScalarAssignment>(*this, e);
                return *this;
            }

            BoundedMatrix& assign(InitializerListType l)
            {
                InitListMatrix<ValueType> ilm(l);
                resize(ilm.getSize1(), ilm.getSize2());
                matrixAssignMatrix<ScalarAssignment>(*this, ilm);
                return *this;
            }

            template <typename E>
            BoundedMatrix& plusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, e);
                return *this;
            }

            BoundedMatrix& plusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            template <typename E>
            BoundedMatrix& minusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, e);
                return *this;
            }

            BoundedMatrix& minusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            void swap(BoundedMatrix& m)
            {
                if (this != &m) {
                    SizeType max_size1 = std::max(size1, m.size1);
                    SizeType max_size2 = std::max(size2, m.size2);

                    for (SizeType i = 0; i < max_size1; i++)
                        std::swap_ranges(data[i], data[i] + max_size2, m.data[i]);

                    std::swap(size1, m.size1);
                    std::swap(size2, m.size2);
                }
            }

            friend void swap(BoundedMatrix& m1, BoundedMatrix& m2)
            {
                m1.swap(m2);
            }

            void clear(const ValueType& v = ValueType())
            {
                for (SizeType i = 0; i < size1; i++)
                    std::fill(data[i], data[i] + size2, v);
            }

            void resize(SizeType m, SizeType n)
            {
                m = CDPL_MATH_CHECK_MAX_SIZE(m, M, Base::SizeError);
                n = CDPL_MATH_CHECK_MAX_SIZE(n, N, Base::SizeError);

                size1 = m;
                size2 = n;
            }

            void resize(SizeType m, SizeType n, const ValueType& v)
            {
                m = CDPL_MATH_CHECK_MAX_SIZE(m, M, Base::SizeError);
                n = CDPL_MATH_CHECK_MAX_SIZE(n, N, Base::SizeError);

                if (n > size2) {
                    SizeType min_size1 = std::min(size1, m);

                    for (SizeType i = 0; i < min_size1; i++)
                        std::fill(data[i] + size2, data[i] + n, v);
                }

                if (m > size1)
                    for (SizeType i = size1; i < m; i++)
                        std::fill(data[i], data[i] + n, v);

                size1 = m;
                size2 = n;
            }

          private:
            SizeType  size1;
            SizeType  size2;
            ArrayType data;
        };

        template <typename T, std::size_t M, std::size_t N>
        const typename BoundedMatrix<T, M, N>::SizeType BoundedMatrix<T, M, N>::MaxSize1;
        template <typename T, std::size_t M, std::size_t N>
        const typename BoundedMatrix<T, M, N>::SizeType BoundedMatrix<T, M, N>::MaxSize2;

        template <typename T, std::size_t M, std::size_t N>
        class CMatrix : public MatrixContainer<CMatrix<T, M, N> >
        {

            typedef CMatrix<T, M, N> SelfType;

          public:
            typedef T              ValueType;
            typedef T&             Reference;
            typedef const T&       ConstReference;
            typedef std::size_t    SizeType;
            typedef std::ptrdiff_t DifferenceType;
            typedef ValueType      ArrayType[M][N];
            typedef T (*ArrayPointer)[N];
            typedef const T (*ConstArrayPointer)[N];
            typedef T*                                               Pointer;
            typedef const T*                                         ConstPointer;
            typedef MatrixReference<SelfType>                        ClosureType;
            typedef const MatrixReference<const SelfType>            ConstClosureType;
            typedef BoundedMatrix<T, M, N>                           MatrixTemporaryType;
            typedef BoundedVector<T, M * N>                          VectorTemporaryType;
            typedef std::shared_ptr<SelfType>                        SharedPointer;
            typedef std::initializer_list<std::initializer_list<T> > InitializerListType;

            static const SizeType Size1 = M;
            static const SizeType Size2 = N;

            CMatrix()
            {
                for (SizeType i = 0; i < M; i++)
                    std::fill(data[i], data[i] + N, ValueType());
            }

            explicit CMatrix(const ValueType& v)
            {
                for (SizeType i = 0; i < M; i++)
                    std::fill(data[i], data[i] + N, v);
            }

            CMatrix(const CMatrix& m)
            {
                for (SizeType i = 0; i < M; i++)
                    std::copy(m.data[i], m.data[i] + N, data[i]);
            }

            CMatrix(InitializerListType l)
            {
                assign(l);
            }

            template <typename E>
            CMatrix(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarAssignment>(*this, e);
            }

            Reference operator()(SizeType i, SizeType j)
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return data[i][j];
            }

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return data[i][j];
            }

            bool isEmpty() const
            {
                return (M == 0 || N == 0);
            }

            SizeType getSize1() const
            {
                return M;
            }

            SizeType getSize2() const
            {
                return N;
            }

            SizeType getMaxSize1() const
            {
                return M;
            }

            SizeType getMaxSize2() const
            {
                return N;
            }

            ArrayPointer getData()
            {
                return data;
            }

            ConstArrayPointer getData() const
            {
                return data;
            }

            CMatrix& operator=(const CMatrix& m)
            {
                if (this != &m) {
                    for (SizeType i = 0; i < M; i++)
                        std::copy(m.data[i], m.data[i] + N, data[i]);
                }

                return *this;
            }

            template <typename C>
            CMatrix& operator=(const MatrixContainer<C>& c)
            {
                return assign(c);
            }

            template <typename T1>
            CMatrix& operator=(InitializerListType l)
            {
                return assign(l);
            }

            template <typename E>
            CMatrix& operator=(const MatrixExpression<E>& e)
            {
                CMatrix      tmp(e);
                return this->operator=(tmp);
            }

            template <typename C>
            CMatrix& operator+=(const MatrixContainer<C>& c)
            {
                return plusAssign(c);
            }

            CMatrix& operator+=(InitializerListType l)
            {
                return plusAssign(l);
            }

            template <typename E>
            CMatrix& operator+=(const MatrixExpression<E>& e)
            {
                CMatrix      tmp(*this + e);
                return this->operator=(tmp);
            }

            template <typename C>
            CMatrix& operator-=(const MatrixContainer<C>& c)
            {
                return minusAssign(c);
            }

            CMatrix& operator-=(InitializerListType l)
            {
                return minusAssign(l);
            }

            template <typename E>
            CMatrix& operator-=(const MatrixExpression<E>& e)
            {
                CMatrix      tmp(*this - e);
                return this->operator=(tmp);
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, CMatrix>::type& operator*=(const T1& t)
            {
                matrixAssignScalar<ScalarMultiplicationAssignment>(*this, t);
                return *this;
            }

            template <typename T1>
            typename std::enable_if<IsScalar<T1>::value, CMatrix>::type& operator/=(const T1& t)
            {
                matrixAssignScalar<ScalarDivisionAssignment>(*this, t);
                return *this;
            }

            template <typename E>
            CMatrix& assign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarAssignment>(*this, e);
                return *this;
            }

            CMatrix& assign(InitializerListType l)
            {
                SizeType n_rows = CDPL_MATH_CHECK_MAX_SIZE(SizeType(l.size()), M, Base::SizeError);

                for (SizeType i = 0; i < n_rows; i++) {
                    const auto& row = *(l.begin() + i);

                    if (row.size() < N) {
                        std::copy(row.begin(), row.end(), data[i]);
                        std::fill(data[i] + row.size(), data[i] + N, ValueType());

                    } else {
                        CDPL_MATH_CHECK_MAX_SIZE(SizeType(row.size()), N, Base::SizeError);
                        std::copy(row.begin(), row.begin() + N, data[i]);
                    }
                }

                for (SizeType i = n_rows; i < M; i++)
                    std::fill(data[i], data[i] + N, ValueType());

                return *this;
            }

            template <typename E>
            CMatrix& plusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, e);
                return *this;
            }

            CMatrix& plusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarAdditionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            template <typename E>
            CMatrix& minusAssign(const MatrixExpression<E>& e)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, e);
                return *this;
            }

            CMatrix& minusAssign(InitializerListType l)
            {
                matrixAssignMatrix<ScalarSubtractionAssignment>(*this, InitListMatrix<ValueType>(l));
                return *this;
            }

            void swap(CMatrix& m)
            {
                if (this != &m) {
                    for (SizeType i = 0; i < M; i++)
                        std::swap_ranges(data[i], data[i] + N, m.data[i]);
                }
            }

            friend void swap(CMatrix& m1, CMatrix& m2)
            {
                m1.swap(m2);
            }

            void clear(const ValueType& v = ValueType())
            {
                for (SizeType i = 0; i < M; i++)
                    std::fill(data[i], data[i] + N, v);
            }

          private:
            ArrayType data;
        };

        template <typename T, std::size_t M, std::size_t N>
        const typename CMatrix<T, M, N>::SizeType CMatrix<T, M, N>::Size1;
        template <typename T, std::size_t M, std::size_t N>
        const typename CMatrix<T, M, N>::SizeType CMatrix<T, M, N>::Size2;

        template <typename T>
        class ZeroMatrix : public MatrixContainer<ZeroMatrix<T> >
        {

            typedef ZeroMatrix<T> SelfType;

          public:
            typedef T                                     ValueType;
            typedef const T&                              Reference;
            typedef const T&                              ConstReference;
            typedef std::size_t                           SizeType;
            typedef std::ptrdiff_t                        DifferenceType;
            typedef MatrixReference<SelfType>             ClosureType;
            typedef const MatrixReference<const SelfType> ConstClosureType;
            typedef Matrix<T>                             MatrixTemporaryType;
            typedef Vector<T, std::vector<T> >            VectorTemporaryType;

            ZeroMatrix():
                size1(0), size2(0) {}

            ZeroMatrix(SizeType m, SizeType n):
                size1(m), size2(n) {}

            ZeroMatrix(const ZeroMatrix& m):
                size1(m.size1), size2(m.size2) {}

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return zero;
            }

            bool isEmpty() const
            {
                return (size1 == 0 || size2 == 0);
            }

            SizeType getSize1() const
            {
                return size1;
            }

            SizeType getSize2() const
            {
                return size2;
            }

            SizeType getMaxSize1() const
            {
                return std::numeric_limits<SizeType>::max();
            }

            SizeType getMaxSize2() const
            {
                return std::numeric_limits<SizeType>::max();
            }

            ZeroMatrix& operator=(const ZeroMatrix& m)
            {
                if (this != &m) {
                    size1 = m.size1;
                    size2 = m.size2;
                }

                return *this;
            }

            void swap(ZeroMatrix& m)
            {
                if (this != &m) {
                    std::swap(size1, m.size1);
                    std::swap(size2, m.size2);
                }
            }

            friend void swap(ZeroMatrix& m1, ZeroMatrix& m2)
            {
                m1.swap(m2);
            }

            void resize(SizeType m, SizeType n)
            {
                size1 = m;
                size2 = n;
            }

          private:
            SizeType               size1;
            SizeType               size2;
            static const ValueType zero;
        };

        template <typename T>
        const typename ZeroMatrix<T>::ValueType ZeroMatrix<T>::zero = ZeroMatrix<T>::ValueType();

        template <typename T>
        class ScalarMatrix : public MatrixContainer<ScalarMatrix<T> >
        {

            typedef ScalarMatrix<T> SelfType;

          public:
            typedef T                                     ValueType;
            typedef const T&                              Reference;
            typedef const T&                              ConstReference;
            typedef std::size_t                           SizeType;
            typedef std::ptrdiff_t                        DifferenceType;
            typedef MatrixReference<SelfType>             ClosureType;
            typedef const MatrixReference<const SelfType> ConstClosureType;
            typedef Matrix<T>                             MatrixTemporaryType;
            typedef Vector<T, std::vector<T> >            VectorTemporaryType;

            ScalarMatrix():
                size1(0), size2(0), value() {}

            ScalarMatrix(SizeType m, SizeType n, const ValueType& v = ValueType()):
                size1(m), size2(n), value(v) {}

            ScalarMatrix(const ScalarMatrix& m):
                size1(m.size1), size2(m.size2), value(m.value) {}

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return value;
            }

            bool isEmpty() const
            {
                return (size1 == 0 || size2 == 0);
            }

            SizeType getSize1() const
            {
                return size1;
            }

            SizeType getSize2() const
            {
                return size2;
            }

            SizeType getMaxSize1() const
            {
                return std::numeric_limits<SizeType>::max();
            }

            SizeType getMaxSize2() const
            {
                return std::numeric_limits<SizeType>::max();
            }

            ScalarMatrix& operator=(const ScalarMatrix& m)
            {
                if (this != &m) {
                    size1 = m.size1;
                    size2 = m.size2;
                    value = m.value;
                }

                return *this;
            }

            void swap(ScalarMatrix& m)
            {
                if (this != &m) {
                    std::swap(size1, m.size1);
                    std::swap(size2, m.size2);
                    std::swap(value, m.value);
                }
            }

            friend void swap(ScalarMatrix& m1, ScalarMatrix& m2)
            {
                m1.swap(m2);
            }

            void resize(SizeType m, SizeType n)
            {
                size1 = m;
                size2 = n;
            }

          private:
            SizeType  size1;
            SizeType  size2;
            ValueType value;
        };

        template <typename T>
        class IdentityMatrix : public MatrixContainer<IdentityMatrix<T> >
        {

            typedef IdentityMatrix<T> SelfType;

          public:
            typedef T                                     ValueType;
            typedef const T&                              Reference;
            typedef const T&                              ConstReference;
            typedef std::size_t                           SizeType;
            typedef std::ptrdiff_t                        DifferenceType;
            typedef MatrixReference<SelfType>             ClosureType;
            typedef const MatrixReference<const SelfType> ConstClosureType;
            typedef Matrix<T>                             MatrixTemporaryType;
            typedef Vector<T, std::vector<T> >            VectorTemporaryType;

            IdentityMatrix():
                size1(0), size2(0) {}

            IdentityMatrix(SizeType m, SizeType n):
                size1(m), size2(n) {}

            IdentityMatrix(const IdentityMatrix& m):
                size1(m.size1), size2(m.size2) {}

            ConstReference operator()(SizeType i, SizeType j) const
            {
                CDPL_MATH_CHECK(i < getSize1() && j < getSize2(), "Index out of range", Base::IndexError);
                return (i == j ? one : zero);
            }

            bool isEmpty() const
            {
                return (size1 == 0 || size2 == 0);
            }

            SizeType getSize1() const
            {
                return size1;
            }

            SizeType getSize2() const
            {
                return size2;
            }

            SizeType getMaxSize1() const
            {
                return std::numeric_limits<SizeType>::max();
            }

            SizeType getMaxSize2() const
            {
                return std::numeric_limits<SizeType>::max();
            }

            IdentityMatrix& operator=(const IdentityMatrix& m)
            {
                if (this != &m) {
                    size1 = m.size1;
                    size2 = m.size2;
                }

                return *this;
            }

            void swap(IdentityMatrix& m)
            {
                if (this != &m) {
                    std::swap(size1, m.size1);
                    std::swap(size2, m.size2);
                }
            }

            friend void swap(IdentityMatrix& m1, IdentityMatrix& m2)
            {
                m1.swap(m2);
            }

            void resize(SizeType m, SizeType n)
            {
                size1 = m;
                size2 = n;
            }

          private:
            SizeType               size1;
            SizeType               size2;
            static const ValueType zero;
            static const ValueType one;
        };

        template <typename T>
        const typename IdentityMatrix<T>::ValueType IdentityMatrix<T>::zero = IdentityMatrix<T>::ValueType();
        template <typename T>
        const typename IdentityMatrix<T>::ValueType IdentityMatrix<T>::one = IdentityMatrix<T>::ValueType(1);

        template <typename M>
        struct VectorTemporaryTraits<MatrixReference<M> > : public VectorTemporaryTraits<M>
        {};

        template <typename M>
        struct VectorTemporaryTraits<const MatrixReference<M> > : public VectorTemporaryTraits<M>
        {};

        template <typename M>
        struct MatrixTemporaryTraits<MatrixReference<M> > : public MatrixTemporaryTraits<M>
        {};

        template <typename M>
        struct MatrixTemporaryTraits<const MatrixReference<M> > : public MatrixTemporaryTraits<M>
        {};

        template <typename E>
        typename E::ValueType
        det(const MatrixExpression<E>& e)
        {
            typedef typename E::ValueType                ValueType;
            typedef typename Matrix<ValueType>::SizeType SizeType;

            Matrix<ValueType>     lu(e);
            std::vector<SizeType> pv(lu.getSize1());
            std::size_t           num_row_swaps;

            luDecompose(lu, pv, num_row_swaps);

            ValueType res(1);
            SizeType  size = std::min(lu.getSize1(), lu.getSize2());

            for (SizeType i = 0; i < size; i++)
                res *= lu(i, i);

            return (num_row_swaps % 2 == 0 ? res : -res);
        }

        template <typename C>
        typename C::ValueType
        det(const MatrixContainer<C>& c)
        {
            typedef typename C::ValueType                   ValueType;
            typedef typename MatrixTemporaryTraits<C>::Type CTemporaryType;
            typedef typename CTemporaryType::SizeType       SizeType;

            CTemporaryType        lu(c);
            std::vector<SizeType> pv(lu.getSize1());
            std::size_t           num_row_swaps;

            luDecompose(lu, pv, num_row_swaps);

            ValueType res(1);
            SizeType  size = std::min(lu.getSize1(), lu.getSize2());

            for (SizeType i = 0; i < size; i++)
                res *= lu(i, i);

            return (num_row_swaps % 2 == 0 ? res : -res);
        }

        template <typename E, typename C>
        bool
        invert(const MatrixExpression<E>& e, MatrixContainer<C>& c)
        {
            typedef typename C::ValueType                   ValueType;
            typedef typename MatrixTemporaryTraits<C>::Type CTemporaryType;
            typedef typename CTemporaryType::SizeType       SizeType;

            CTemporaryType        lu(e);
            std::vector<SizeType> pv(lu.getSize1());
            std::size_t           num_row_swaps;

            if (luDecompose(lu, pv, num_row_swaps) > 0)
                return false;

            c().assign(IdentityMatrix<ValueType>(lu.getSize1(), lu.getSize2()));

            return luSubstitute(lu, pv, c);
        }

        template <typename C>
        bool
        invert(MatrixContainer<C>& c)
        {
            return invert(c, c);
        }

        typedef ZeroMatrix<float>         FZeroMatrix;
        typedef ZeroMatrix<double>        DZeroMatrix;
        typedef ZeroMatrix<long>          LZeroMatrix;
        typedef ZeroMatrix<unsigned long> ULZeroMatrix;

        typedef ScalarMatrix<float>         FScalarMatrix;
        typedef ScalarMatrix<double>        DScalarMatrix;
        typedef ScalarMatrix<long>          LScalarMatrix;
        typedef ScalarMatrix<unsigned long> ULScalarMatrix;

        typedef IdentityMatrix<float>         FIdentityMatrix;
        typedef IdentityMatrix<double>        DIdentityMatrix;
        typedef IdentityMatrix<long>          LIdentityMatrix;
        typedef IdentityMatrix<unsigned long> ULIdentityMatrix;

        /**
         * \brief An unbounded dense matrix holding floating point values of type <tt>float</tt>..
         */
        typedef Matrix<float> FMatrix;

        /**
         * \brief An unbounded dense matrix holding floating point values of type <tt>double</tt>..
         */
        typedef Matrix<double> DMatrix;

        /**
         * \brief An unbounded dense matrix holding signed integers of type <tt>long</tt>.
         */
        typedef Matrix<long> LMatrix;

        /**
         * \brief An unbounded dense matrix holding unsigned integers of type <tt>unsigned long</tt>.
         */
        typedef Matrix<unsigned long> ULMatrix;

        /**
         * \brief A bounded 2x2 matrix holding floating point values of type <tt>float</tt>.
         */
        typedef CMatrix<float, 2, 2> Matrix2F;

        /**
         * \brief A bounded 3x3 matrix holding floating point values of type <tt>float</tt>.
         */
        typedef CMatrix<float, 3, 3> Matrix3F;

        /**
         * \brief A bounded 4x4 matrix holding floating point values of type <tt>float</tt>.
         */
        typedef CMatrix<float, 4, 4> Matrix4F;

        /**
         * \brief A bounded 2x2 matrix holding floating point values of type <tt>double</tt>.
         */
        typedef CMatrix<double, 2, 2> Matrix2D;

        /**
         * \brief A bounded 3x3 matrix holding floating point values of type <tt>double</tt>.
         */
        typedef CMatrix<double, 3, 3> Matrix3D;

        /**
         * \brief A bounded 4x4 matrix holding floating point values of type <tt>double</tt>.
         */
        typedef CMatrix<double, 4, 4> Matrix4D;

        /**
         * \brief A bounded 2x2 matrix holding signed integers of type <tt>long</tt>.
         */
        typedef CMatrix<long, 2, 2> Matrix2L;

        /**
         * \brief A bounded 3x3 matrix holding signed integers of type <tt>long</tt>.
         */
        typedef CMatrix<long, 3, 3> Matrix3L;

        /**
         * \brief A bounded 4x4 matrix holding signed integers of type <tt>long</tt>.
         */
        typedef CMatrix<long, 4, 4> Matrix4L;

        /**
         * \brief A bounded 2x2 matrix holding unsigned integers of type <tt>unsigned long</tt>.
         */
        typedef CMatrix<unsigned long, 2, 2> Matrix2UL;

        /**
         * \brief A bounded 3x3 matrix holding unsigned integers of type <tt>unsigned long</tt>.
         */
        typedef CMatrix<unsigned long, 3, 3> Matrix3UL;

        /**
         * \brief A bounded 4x4 matrix holding unsigned integers of type <tt>unsigned long</tt>.
         */
        typedef CMatrix<unsigned long, 4, 4> Matrix4UL;

        /**
         * \brief An unbounded sparse matrix holding floating point values of type <tt>float</tt>..
         */
        typedef SparseMatrix<float> SparseFMatrix;

        /**
         * \brief An unbounded sparse matrix holding floating point values of type <tt>double</tt>..
         */
        typedef SparseMatrix<double> SparseDMatrix;

        /**
         * \brief An unbounded sparse matrix holding signed integers of type <tt>long</tt>.
         */
        typedef SparseMatrix<long> SparseLMatrix;

        /**
         * \brief An unbounded sparse matrix holding unsigned integers of type <tt>unsigned long</tt>.
         */
        typedef SparseMatrix<unsigned long> SparseULMatrix;
    } // namespace Math
} // namespace CDPL

#endif // CDPL_MATH_MATRIX_HPP
