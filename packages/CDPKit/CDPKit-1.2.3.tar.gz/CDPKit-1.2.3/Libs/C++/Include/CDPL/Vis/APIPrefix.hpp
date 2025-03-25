/* 
 * APIPrefix.hpp 
 *
 * This file is part of the Chemical Data Processing Toolkit
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
 * \brief Definition of the preprocessor macro \ref CDPL_VIS_API.
 */

#ifndef CDPL_VIS_APIPREFIX_HPP
#define CDPL_VIS_APIPREFIX_HPP

#ifdef CDPL_VIS_STATIC_LINK
# define CDPL_VIS_API
#else // CDPL_VIS_STATIC_LINK
# include "CDPL/APIPrefix.hpp"
# ifdef cdpl_vis_shared_EXPORTS
#  define CDPL_VIS_API CDPL_API_EXPORT
# else
#  define CDPL_VIS_API CDPL_API_IMPORT
# endif // cdpl_vis_shared_EXPORTS
#endif // CDPL_VIS_STATIC_LINK

#ifdef CDPL_VIS_QT_STATIC_LINK
# define CDPL_VIS_QT_API
#else // CDPL_VIS_QT_STATIC_LINK
# include "CDPL/APIPrefix.hpp"
# ifdef cdpl_vis_qt_shared_EXPORTS
#  define CDPL_VIS_QT_API CDPL_API_EXPORT
# else
#  define CDPL_VIS_QT_API CDPL_API_IMPORT
# endif // cdpl_vis_qt_shared_EXPORTS
#endif // CDPL_VIS_QT_STATIC_LINK

/**
 * \def CDPL_VIS_API
 * \brief Tells the compiler/linker which classes, functions and variables are part of the library API.
 */

/**
 * \def CDPL_VIS_QT_API
 * \brief Tells the compiler/linker which classes, functions and variables are part of the library API.
 */

#endif // CDPL_VIS_APIPREFIX_HPP
