/* 
 * VectorProxy.hpp 
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
 * \brief Definition of vector proxy types.
 */

#ifndef CDPL_MATH_VECTORPROXY_HPP
#define CDPL_MATH_VECTORPROXY_HPP

#include <type_traits>

#include "CDPL/Math/Expression.hpp"
#include "CDPL/Math/VectorAssignment.hpp"
#include "CDPL/Math/TypeTraits.hpp"
#include "CDPL/Math/Functional.hpp"
#include "CDPL/Math/Range.hpp"
#include "CDPL/Math/Slice.hpp"


namespace CDPL
{

    namespace Math
    {

        template <typename V>
        class VectorRange : public VectorExpression<VectorRange<V> >
        {

            typedef VectorRange<V> SelfType;

          public:
            typedef V                                                        VectorType;
            typedef typename V::SizeType                                     SizeType;
            typedef typename V::DifferenceType                               DifferenceType;
            typedef typename V::ValueType                                    ValueType;
            typedef typename V::ConstReference                               ConstReference;
            typedef typename std::conditional<std::is_const<V>::value,
                                              typename V::ConstReference,
                                              typename V::Reference>::type   Reference;
            typedef typename std::conditional<std::is_const<V>::value,
                                              typename V::ConstClosureType,
                                              typename V::ClosureType>::type VectorClosureType;
            typedef const SelfType                                           ConstClosureType;
            typedef SelfType                                                 ClosureType;
            typedef Range<SizeType>                                          RangeType;

            VectorRange(VectorType& v, const RangeType& r):
                data(v), range(r) {}

            Reference operator()(SizeType i)
            {
                return data(range(i));
            }

            ConstReference operator()(SizeType i) const
            {
                return data(range(i));
            }

            Reference operator[](SizeType i)
            {
                return data[range(i)];
            }

            ConstReference operator[](SizeType i) const
            {
                return data[range(i)];
            }

            SizeType getStart() const
            {
                return range.getStart();
            }

            SizeType getSize() const
            {
                return range.getSize();
            }

            bool isEmpty() const
            {
                return range.isEmpty();
            }

            VectorClosureType& getData()
            {
                return data;
            }

            const VectorClosureType& getData() const
            {
                return data;
            }

            VectorRange& operator=(const VectorRange& r)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(r));
                return *this;
            }

            template <typename E>
            VectorRange& operator=(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(e));
                return *this;
            }

            template <typename E>
            VectorRange& operator+=(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(*this + e));
                return *this;
            }

            template <typename E>
            VectorRange& operator-=(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(*this - e));
                return *this;
            }

            template <typename T>
            typename std::enable_if<IsScalar<T>::value, VectorRange>::type& operator*=(const T& t)
            {
                vectorAssignScalar<ScalarMultiplicationAssignment>(*this, t);
                return *this;
            }

            template <typename T>
            typename std::enable_if<IsScalar<T>::value, VectorRange>::type& operator/=(const T& t)
            {
                vectorAssignScalar<ScalarDivisionAssignment>(*this, t);
                return *this;
            }

            template <typename E>
            VectorRange& assign(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, e);
                return *this;
            }

            template <typename E>
            VectorRange& plusAssign(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAdditionAssignment>(*this, e);
                return *this;
            }

            template <typename E>
            VectorRange& minusAssign(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarSubtractionAssignment>(*this, e);
                return *this;
            }

            void swap(VectorRange& r)
            {
                if (this != &r)
                    vectorSwap(*this, r);
            }

            friend void swap(VectorRange& r1, VectorRange& r2)
            {
                r1.swap(r2);
            }

          private:
            VectorClosureType data;
            RangeType         range;
        };

        template <typename V>
        class VectorSlice : public VectorExpression<VectorSlice<V> >
        {

            typedef VectorSlice<V> SelfType;

          public:
            typedef V                                                        VectorType;
            typedef typename V::SizeType                                     SizeType;
            typedef typename V::DifferenceType                               DifferenceType;
            typedef typename V::ValueType                                    ValueType;
            typedef typename V::ConstReference                               ConstReference;
            typedef typename std::conditional<std::is_const<V>::value,
                                              typename V::ConstReference,
                                              typename V::Reference>::type   Reference;
            typedef typename std::conditional<std::is_const<V>::value,
                                              typename V::ConstClosureType,
                                              typename V::ClosureType>::type VectorClosureType;
            typedef const SelfType                                           ConstClosureType;
            typedef SelfType                                                 ClosureType;
            typedef Slice<SizeType, DifferenceType>                          SliceType;

            VectorSlice(VectorType& v, const SliceType& s):
                data(v), slice(s) {}

            Reference operator()(SizeType i)
            {
                return data(slice(i));
            }

            ConstReference operator()(SizeType i) const
            {
                return data(slice(i));
            }

            Reference operator[](SizeType i)
            {
                return data[slice(i)];
            }

            ConstReference operator[](SizeType i) const
            {
                return data[slice(i)];
            }

            SizeType getStart() const
            {
                return slice.getStart();
            }

            DifferenceType getStride() const
            {
                return slice.getStride();
            }

            SizeType getSize() const
            {
                return slice.getSize();
            }

            bool isEmpty() const
            {
                return slice.isEmpty();
            }

            VectorClosureType& getData()
            {
                return data;
            }

            const VectorClosureType& getData() const
            {
                return data;
            }

            VectorSlice& operator=(const VectorSlice& s)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(s));
                return *this;
            }

            template <typename E>
            VectorSlice& operator=(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(e));
                return *this;
            }

            template <typename E>
            VectorSlice& operator+=(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(*this + e));
                return *this;
            }

            template <typename E>
            VectorSlice& operator-=(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, typename VectorTemporaryTraits<V>::Type(*this - e));
                return *this;
            }

            template <typename T>
            typename std::enable_if<IsScalar<T>::value, VectorSlice>::type& operator*=(const T& t)
            {
                vectorAssignScalar<ScalarMultiplicationAssignment>(*this, t);
                return *this;
            }

            template <typename T>
            typename std::enable_if<IsScalar<T>::value, VectorSlice>::type& operator/=(const T& t)
            {
                vectorAssignScalar<ScalarDivisionAssignment>(*this, t);
                return *this;
            }

            template <typename E>
            VectorSlice& assign(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAssignment>(*this, e);
                return *this;
            }

            template <typename E>
            VectorSlice& plusAssign(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarAdditionAssignment>(*this, e);
                return *this;
            }

            template <typename E>
            VectorSlice& minusAssign(const VectorExpression<E>& e)
            {
                vectorAssignVector<ScalarSubtractionAssignment>(*this, e);
                return *this;
            }

            void swap(VectorSlice& s)
            {
                if (this != &s)
                    vectorSwap(*this, s);
            }

            friend void swap(VectorSlice& s1, VectorSlice& s2)
            {
                s1.swap(s2);
            }

          private:
            VectorClosureType data;
            SliceType         slice;
        };

        template <typename V>
        struct VectorTemporaryTraits<VectorRange<V> > : public VectorTemporaryTraits<V>
        {};

        template <typename V>
        struct VectorTemporaryTraits<const VectorRange<V> > : public VectorTemporaryTraits<V>
        {};

        template <typename V>
        struct VectorTemporaryTraits<VectorSlice<V> > : public VectorTemporaryTraits<V>
        {};

        template <typename V>
        struct VectorTemporaryTraits<const VectorSlice<V> > : public VectorTemporaryTraits<V>
        {};

        template <typename E>
        VectorRange<E>
        range(VectorExpression<E>& e, const typename VectorRange<E>::RangeType& r)
        {
            return VectorRange<E>(e(), r);
        }

        template <typename E>
        VectorRange<const E>
        range(const VectorExpression<E>& e, const typename VectorRange<const E>::RangeType& r)
        {
            return VectorRange<const E>(e(), r);
        }

        template <typename E>
        VectorRange<E>
        range(VectorExpression<E>&                         e,
              typename VectorRange<E>::RangeType::SizeType start,
              typename VectorRange<E>::RangeType::SizeType stop)
        {
            typedef typename VectorRange<E>::RangeType RangeType;

            return VectorRange<E>(e(), RangeType(start, stop));
        }

        template <typename E>
        VectorRange<const E>
        range(const VectorExpression<E>&                         e,
              typename VectorRange<const E>::RangeType::SizeType start,
              typename VectorRange<const E>::RangeType::SizeType stop)
        {
            typedef typename VectorRange<const E>::RangeType RangeType;

            return VectorRange<const E>(e(), RangeType(start, stop));
        }

        template <typename E>
        VectorSlice<E>
        slice(VectorExpression<E>& e, const typename VectorSlice<E>::SliceType& s)
        {
            return VectorSlice<E>(e(), s);
        }

        template <typename E>
        VectorSlice<const E>
        slice(const VectorExpression<E>& e, const typename VectorSlice<const E>::SliceType& s)
        {
            return VectorSlice<const E>(e(), s);
        }

        template <typename E>
        VectorSlice<E>
        slice(VectorExpression<E>&                               e,
              typename VectorSlice<E>::SliceType::SizeType       start,
              typename VectorSlice<E>::SliceType::DifferenceType stride,
              typename VectorSlice<E>::SliceType::SizeType       size)
        {
            typedef typename VectorSlice<E>::SliceType SliceType;

            return VectorSlice<E>(e(), SliceType(start, stride, size));
        }

        template <typename E>
        VectorSlice<const E>
        slice(const VectorExpression<E>&                               e,
              typename VectorSlice<const E>::SliceType::SizeType       start,
              typename VectorSlice<const E>::SliceType::DifferenceType stride,
              typename VectorSlice<const E>::SliceType::SizeType       size)
        {
            typedef typename VectorSlice<const E>::SliceType SliceType;

            return VectorSlice<const E>(e(), SliceType(start, stride, size));
        }
    } // namespace Math
} // namespace CDPL

#endif // CDPL_MATH_VECTORPROXY_HPP
