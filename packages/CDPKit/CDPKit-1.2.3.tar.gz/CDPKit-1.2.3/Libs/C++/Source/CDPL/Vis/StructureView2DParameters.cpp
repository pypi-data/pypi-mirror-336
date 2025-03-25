/* 
 * StructureView2DParameters.cpp 
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


#include "StaticInit.hpp"

#include <functional>

#include "CDPL/Vis/View2D.hpp"
#include "CDPL/Vis/ControlParameter.hpp"
#include "CDPL/Vis/ControlParameterDefault.hpp"

#include "StructureView2DParameters.hpp"


using namespace CDPL;


Vis::StructureView2DParameters::StructureView2DParameters(View2D& view): 
    view(view),
    viewport(ControlParameterDefault::VIEWPORT),
    stdBondLength(ControlParameterDefault::BOND_LENGTH.getValue()),
    sizeAdjustment(ControlParameterDefault::SIZE_ADJUSTMENT),
    alignment(ControlParameterDefault::ALIGNMENT),
    backgroundBrush(ControlParameterDefault::BACKGROUND_BRUSH),
    useCalcAtomCoordsFlag(ControlParameterDefault::USE_CALCULATED_ATOM_COORDINATES),
    atomColor(ControlParameterDefault::ATOM_COLOR),
    atomLabelFont(ControlParameterDefault::ATOM_LABEL_FONT),
    secondaryAtomLabelFont(ControlParameterDefault::SECONDARY_ATOM_LABEL_FONT),
    atomConfigLabelFont(ControlParameterDefault::ATOM_CONFIGURATION_LABEL_FONT),
    atomCustomLabelFont(ControlParameterDefault::ATOM_CUSTOM_LABEL_FONT),
    atomConfigLabelColor(ControlParameterDefault::ATOM_CONFIGURATION_LABEL_COLOR),
    atomCustomLabelColor(ControlParameterDefault::ATOM_CUSTOM_LABEL_COLOR),
    atomLabelSize(ControlParameterDefault::ATOM_LABEL_SIZE),
    secondaryAtomLabelSize(ControlParameterDefault::SECONDARY_ATOM_LABEL_SIZE),
    atomConfigLabelSize(ControlParameterDefault::ATOM_CONFIGURATION_LABEL_SIZE),
    atomCustomLabelSize(ControlParameterDefault::ATOM_CUSTOM_LABEL_SIZE),
    atomLabelMargin(ControlParameterDefault::ATOM_LABEL_MARGIN),
    radicalElectronDotSize(ControlParameterDefault::RADICAL_ELECTRON_DOT_SIZE),
    atomHighlightAreaSize(ControlParameterDefault::ATOM_HIGHLIGHT_AREA_SIZE),
    atomHighlightAreaBrush(ControlParameterDefault::ATOM_HIGHLIGHT_AREA_BRUSH),
    atomHighlightAreaPen(ControlParameterDefault::ATOM_HIGHLIGHT_AREA_OUTLINE_PEN),
    breakAtomHighltAreaOutline(ControlParameterDefault::BREAK_ATOM_HIGHLIGHT_AREA_OUTLINE),
    showCarbonsFlag(ControlParameterDefault::SHOW_CARBONS),
    showChargesFlag(ControlParameterDefault::SHOW_CHARGES),
    showIsotopesFlag(ControlParameterDefault::SHOW_ISOTOPES),
    showExplicitHsFlag(ControlParameterDefault::SHOW_EXPLICIT_HYDROGENS),
    showHydrogenCountsFlag(ControlParameterDefault::SHOW_HYDROGEN_COUNTS),
    showNonCarbonHydrogenCountsFlag(ControlParameterDefault::SHOW_NON_CARBON_HYDROGEN_COUNTS),
    showAtomReactionInfosFlag(ControlParameterDefault::SHOW_ATOM_REACTION_INFOS),
    showAtomQueryInfosFlag(ControlParameterDefault::SHOW_ATOM_QUERY_INFOS),
    showRadicalElectronsFlag(ControlParameterDefault::SHOW_RADICAL_ELECTRONS),
    showAtomConfigLabelsFlag(ControlParameterDefault::SHOW_ATOM_CONFIGURATION_LABELS),
    showAtomCustomLabelsFlag(ControlParameterDefault::SHOW_ATOM_CUSTOM_LABELS),
    enableAtomHighlightingFlag(ControlParameterDefault::ENABLE_ATOM_HIGHLIGHTING),
    highlightAreaOutlineWidth(ControlParameterDefault::HIGHLIGHT_AREA_OUTLINE_WIDTH),
    bondColor(ControlParameterDefault::BOND_COLOR),
    bondLabelFont(ControlParameterDefault::BOND_LABEL_FONT),
    bondConfigLabelFont(ControlParameterDefault::BOND_CONFIGURATION_LABEL_FONT),
    bondCustomLabelFont(ControlParameterDefault::BOND_CUSTOM_LABEL_FONT),
    bondConfigLabelColor(ControlParameterDefault::BOND_CONFIGURATION_LABEL_COLOR),
    bondCustomLabelColor(ControlParameterDefault::BOND_CUSTOM_LABEL_COLOR),
    bondLabelSize(ControlParameterDefault::BOND_LABEL_SIZE),
    bondConfigLabelSize(ControlParameterDefault::BOND_CONFIGURATION_LABEL_SIZE),
    bondCustomLabelSize(ControlParameterDefault::BOND_CUSTOM_LABEL_SIZE),
    bondLabelMargin(ControlParameterDefault::BOND_LABEL_MARGIN),
    bondLineWidth(ControlParameterDefault::BOND_LINE_WIDTH),
    bondLineSpacing(ControlParameterDefault::BOND_LINE_SPACING),
    stereoBondWedgeWidth(ControlParameterDefault::STEREO_BOND_WEDGE_WIDTH),
    stereoBondHashSpacing(ControlParameterDefault::STEREO_BOND_HASH_SPACING),
    reactionCenterLineLength(ControlParameterDefault::REACTION_CENTER_LINE_LENGTH),
    reactionCenterLineSpacing(ControlParameterDefault::REACTION_CENTER_LINE_SPACING),
    doubleBondTrimLength(ControlParameterDefault::DOUBLE_BOND_TRIM_LENGTH),
    tripleBondTrimLength(ControlParameterDefault::TRIPLE_BOND_TRIM_LENGTH),
    bondHighlightAreaWidth(ControlParameterDefault::BOND_HIGHLIGHT_AREA_WIDTH),
    bondHighlightAreaBrush(ControlParameterDefault::BOND_HIGHLIGHT_AREA_BRUSH),
    bondHighlightAreaPen(ControlParameterDefault::BOND_HIGHLIGHT_AREA_OUTLINE_PEN),
    showBondReactionInfosFlag(ControlParameterDefault::SHOW_BOND_REACTION_INFOS),
    showBondQueryInfosFlag(ControlParameterDefault::SHOW_BOND_QUERY_INFOS),
    showStereoBondsFlag(ControlParameterDefault::SHOW_STEREO_BONDS),
    showBondConfigLabelsFlag(ControlParameterDefault::SHOW_BOND_CONFIGURATION_LABELS),
    showBondCustomLabelsFlag(ControlParameterDefault::SHOW_BOND_CUSTOM_LABELS),
    enableBondHighlightingFlag(ControlParameterDefault::ENABLE_BOND_HIGHLIGHTING),
    coordinatesChangedFlag(true),
    explicitHVisibilityChangedFlag(true),
    propertyVisibilityChangedFlag(true),
    graphicsAttributeChangedFlag(true),
    stdBondLengthChangedFlag(true),
    viewportChangedFlag(true),
    alignmentChangedFlag(true),
    sizeAdjustmentChangedFlag(true) 
{
    using namespace std::placeholders;
    
    view.registerParameterRemovedCallback(std::bind(&StructureView2DParameters::parameterRemoved, this, _1));
    view.registerParameterChangedCallback(std::bind(&StructureView2DParameters::parameterChanged, this, _1, _2));
    view.registerParentChangedCallback(std::bind(&StructureView2DParameters::parentChanged, this));
}

Vis::StructureView2DParameters::~StructureView2DParameters() {}

const Vis::Rectangle2D& Vis::StructureView2DParameters::getViewport() const
{
    return viewport;
}

unsigned int Vis::StructureView2DParameters::getAlignment() const
{
    return alignment;
}

double Vis::StructureView2DParameters::getStdBondLength() const
{
    return stdBondLength;
}

unsigned int Vis::StructureView2DParameters::getSizeAdjustment() const
{
    return sizeAdjustment;
}

const Vis::Brush& Vis::StructureView2DParameters::getBackgroundBrush() const
{
    return backgroundBrush;
}
            
const Vis::ColorTable::SharedPointer& Vis::StructureView2DParameters::getAtomColorTable() const
{
    return atomColorTable;
}

bool Vis::StructureView2DParameters::useCalculatedAtomCoords() const
{
    return useCalcAtomCoordsFlag;
}

const Vis::Color& Vis::StructureView2DParameters::getAtomColor() const
{
    return atomColor;
}

const Vis::Font& Vis::StructureView2DParameters::getAtomLabelFont() const
{
    return atomLabelFont;
}

const Vis::Font& Vis::StructureView2DParameters::getSecondaryAtomLabelFont() const
{
    return secondaryAtomLabelFont;
}

const Vis::Font& Vis::StructureView2DParameters::getAtomConfigLabelFont() const
{
    return atomConfigLabelFont;
}

const Vis::Font& Vis::StructureView2DParameters::getAtomCustomLabelFont() const
{
    return atomCustomLabelFont;
}

const Vis::Color& Vis::StructureView2DParameters::getAtomConfigLabelColor() const
{
    return atomConfigLabelColor;
}

const Vis::Color& Vis::StructureView2DParameters::getAtomCustomLabelColor() const
{
    return atomCustomLabelColor;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getAtomLabelSize() const
{
    return atomLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getSecondaryAtomLabelSize() const
{
    return secondaryAtomLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getAtomConfigLabelSize() const
{
    return atomConfigLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getAtomCustomLabelSize() const
{
    return atomCustomLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getAtomLabelMargin() const
{
    return atomLabelMargin;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getRadicalElectronDotSize() const
{
    return radicalElectronDotSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getAtomHighlightAreaSize() const
{
    return atomHighlightAreaSize;
}

const Vis::Brush& Vis::StructureView2DParameters::getAtomHighlightAreaBrush() const
{
    return atomHighlightAreaBrush;
}

const Vis::Pen& Vis::StructureView2DParameters::getAtomHighlightAreaPen() const
{
    return atomHighlightAreaPen;
}

bool Vis::StructureView2DParameters::breakAtomHighlightAreaOutline() const
{
    return breakAtomHighltAreaOutline;
}

bool Vis::StructureView2DParameters::showCarbons() const
{
    return showCarbonsFlag;
}

bool Vis::StructureView2DParameters::showIsotopes() const
{
    return showIsotopesFlag;
}

bool Vis::StructureView2DParameters::showCharges() const
{
    return showChargesFlag;
}

bool Vis::StructureView2DParameters::showExplicitHydrogens() const
{
    return showExplicitHsFlag;
}

bool Vis::StructureView2DParameters::showHydrogenCounts() const
{
    return showHydrogenCountsFlag;
}

bool Vis::StructureView2DParameters::showNonCarbonHydrogenCounts() const
{
    return showNonCarbonHydrogenCountsFlag;
}

bool Vis::StructureView2DParameters::showAtomReactionInfos() const
{
    return showAtomReactionInfosFlag;
}

bool Vis::StructureView2DParameters::showAtomQueryInfos() const
{
    return showAtomQueryInfosFlag;
}

bool Vis::StructureView2DParameters::showRadicalElectrons() const
{
    return showRadicalElectronsFlag;
}

bool Vis::StructureView2DParameters::showAtomConfigLabels() const
{
    return showAtomConfigLabelsFlag;
}

bool Vis::StructureView2DParameters::showAtomCustomLabels() const
{
    return showAtomCustomLabelsFlag;
}

bool Vis::StructureView2DParameters::enableAtomHighlighting() const
{
    return enableAtomHighlightingFlag;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getHighlightAreaOutlineWidth() const
{
    return highlightAreaOutlineWidth;
}

const Vis::Color& Vis::StructureView2DParameters::getBondColor() const
{
    return bondColor;
}

const Vis::Font& Vis::StructureView2DParameters::getBondLabelFont() const
{
    return bondLabelFont;
}

const Vis::Font& Vis::StructureView2DParameters::getBondConfigLabelFont() const
{
    return bondConfigLabelFont;
}

const Vis::Font& Vis::StructureView2DParameters::getBondCustomLabelFont() const
{
    return bondCustomLabelFont;
}

const Vis::Color& Vis::StructureView2DParameters::getBondConfigLabelColor() const
{
    return bondConfigLabelColor;
}

const Vis::Color& Vis::StructureView2DParameters::getBondCustomLabelColor() const
{
    return bondCustomLabelColor;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondLabelSize() const
{
    return bondLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondConfigLabelSize() const
{
    return bondConfigLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondCustomLabelSize() const
{
    return bondCustomLabelSize;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondLabelMargin() const
{
    return bondLabelMargin;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondLineWidth() const
{
    return bondLineWidth;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondLineSpacing() const
{
    return bondLineSpacing;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getStereoBondWedgeWidth() const
{
    return stereoBondWedgeWidth;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getStereoBondHashSpacing() const
{
    return stereoBondHashSpacing;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getReactionCenterLineLength() const
{
    return reactionCenterLineLength;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getReactionCenterLineSpacing() const
{
    return reactionCenterLineSpacing;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getDoubleBondTrimLength() const
{
    return doubleBondTrimLength;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getTripleBondTrimLength() const
{
    return tripleBondTrimLength;
}

const Vis::SizeSpecification& Vis::StructureView2DParameters::getBondHighlightAreaWidth() const
{
    return bondHighlightAreaWidth;
}

const Vis::Brush& Vis::StructureView2DParameters::getBondHighlightAreaBrush() const
{
    return bondHighlightAreaBrush;
}

const Vis::Pen& Vis::StructureView2DParameters::getBondHighlightAreaPen() const
{
    return bondHighlightAreaPen;
}

bool Vis::StructureView2DParameters::showBondReactionInfos() const
{
    return showBondReactionInfosFlag;
}

bool Vis::StructureView2DParameters::showBondQueryInfos() const
{
    return showBondQueryInfosFlag;
}

bool Vis::StructureView2DParameters::showStereoBonds() const
{
    return showStereoBondsFlag;
}

bool Vis::StructureView2DParameters::showBondConfigLabels() const
{
    return showBondConfigLabelsFlag;
}

bool Vis::StructureView2DParameters::showBondCustomLabels() const
{
    return showBondCustomLabelsFlag;
}

bool Vis::StructureView2DParameters::enableBondHighlighting() const
{
    return enableBondHighlightingFlag;
}

bool Vis::StructureView2DParameters::coordinatesChanged() const
{
    return coordinatesChangedFlag;
}

bool Vis::StructureView2DParameters::explicitHVisibilityChanged() const
{
    return explicitHVisibilityChangedFlag;
}

bool Vis::StructureView2DParameters::propertyVisibilityChanged() const
{
    return propertyVisibilityChangedFlag;
}

bool Vis::StructureView2DParameters::graphicsAttributeChanged() const
{
    return graphicsAttributeChangedFlag;
}

bool Vis::StructureView2DParameters::stdBondLengthChanged() const
{
    return stdBondLengthChangedFlag;
}

bool Vis::StructureView2DParameters::viewportChanged() const
{
    return viewportChangedFlag;
}

bool Vis::StructureView2DParameters::alignmentChanged() const
{
    return alignmentChangedFlag;
}

bool Vis::StructureView2DParameters::sizeAdjustmentChanged() const
{
    return sizeAdjustmentChangedFlag;
}

void Vis::StructureView2DParameters::clearChangeFlags()
{
    coordinatesChangedFlag         = false;
    explicitHVisibilityChangedFlag = false;
    propertyVisibilityChangedFlag  = false;
    graphicsAttributeChangedFlag   = false;
    stdBondLengthChangedFlag       = false;
    viewportChangedFlag            = false;
    alignmentChangedFlag           = false;
    sizeAdjustmentChangedFlag      = false;
}

void Vis::StructureView2DParameters::parentChanged()
{
    parameterChanged(ControlParameter::VIEWPORT, view.getParameter(ControlParameter::VIEWPORT));
    parameterChanged(ControlParameter::SIZE_ADJUSTMENT, view.getParameter(ControlParameter::SIZE_ADJUSTMENT));
    parameterChanged(ControlParameter::BOND_LENGTH, view.getParameter(ControlParameter::BOND_LENGTH));
    parameterChanged(ControlParameter::ALIGNMENT, view.getParameter(ControlParameter::ALIGNMENT));

    parameterChanged(ControlParameter::BACKGROUND_BRUSH, view.getParameter(ControlParameter::BACKGROUND_BRUSH));
    parameterChanged(ControlParameter::ATOM_COLOR_TABLE, view.getParameter(ControlParameter::ATOM_COLOR_TABLE));
    parameterChanged(ControlParameter::USE_CALCULATED_ATOM_COORDINATES, view.getParameter(ControlParameter::USE_CALCULATED_ATOM_COORDINATES));

    parameterChanged(ControlParameter::ATOM_COLOR, view.getParameter(ControlParameter::ATOM_COLOR));
    parameterChanged(ControlParameter::ATOM_LABEL_FONT, view.getParameter(ControlParameter::ATOM_LABEL_FONT));
    parameterChanged(ControlParameter::ATOM_LABEL_SIZE, view.getParameter(ControlParameter::ATOM_LABEL_SIZE));
    parameterChanged(ControlParameter::SECONDARY_ATOM_LABEL_FONT, view.getParameter(ControlParameter::SECONDARY_ATOM_LABEL_FONT));
    parameterChanged(ControlParameter::SECONDARY_ATOM_LABEL_SIZE, view.getParameter(ControlParameter::SECONDARY_ATOM_LABEL_SIZE));
    parameterChanged(ControlParameter::ATOM_CONFIGURATION_LABEL_FONT, view.getParameter(ControlParameter::ATOM_CONFIGURATION_LABEL_FONT));
    parameterChanged(ControlParameter::ATOM_CONFIGURATION_LABEL_COLOR, view.getParameter(ControlParameter::ATOM_CONFIGURATION_LABEL_COLOR));
    parameterChanged(ControlParameter::ATOM_CONFIGURATION_LABEL_SIZE, view.getParameter(ControlParameter::ATOM_CONFIGURATION_LABEL_SIZE));
    parameterChanged(ControlParameter::ATOM_CUSTOM_LABEL_FONT, view.getParameter(ControlParameter::ATOM_CUSTOM_LABEL_FONT));
    parameterChanged(ControlParameter::ATOM_CUSTOM_LABEL_COLOR, view.getParameter(ControlParameter::ATOM_CUSTOM_LABEL_COLOR));
    parameterChanged(ControlParameter::ATOM_CUSTOM_LABEL_SIZE, view.getParameter(ControlParameter::ATOM_CUSTOM_LABEL_SIZE));
    parameterChanged(ControlParameter::ATOM_LABEL_MARGIN, view.getParameter(ControlParameter::ATOM_LABEL_MARGIN));
    parameterChanged(ControlParameter::RADICAL_ELECTRON_DOT_SIZE, view.getParameter(ControlParameter::RADICAL_ELECTRON_DOT_SIZE));
    parameterChanged(ControlParameter::ATOM_HIGHLIGHT_AREA_SIZE, view.getParameter(ControlParameter::ATOM_HIGHLIGHT_AREA_SIZE));
    parameterChanged(ControlParameter::ATOM_HIGHLIGHT_AREA_BRUSH, view.getParameter(ControlParameter::ATOM_HIGHLIGHT_AREA_BRUSH));
    parameterChanged(ControlParameter::ATOM_HIGHLIGHT_AREA_OUTLINE_PEN, view.getParameter(ControlParameter::ATOM_HIGHLIGHT_AREA_OUTLINE_PEN));
    parameterChanged(ControlParameter::BREAK_ATOM_HIGHLIGHT_AREA_OUTLINE, view.getParameter(ControlParameter::BREAK_ATOM_HIGHLIGHT_AREA_OUTLINE));
    parameterChanged(ControlParameter::SHOW_CARBONS, view.getParameter(ControlParameter::SHOW_CARBONS));
    parameterChanged(ControlParameter::SHOW_CHARGES, view.getParameter(ControlParameter::SHOW_CHARGES));
    parameterChanged(ControlParameter::SHOW_ISOTOPES, view.getParameter(ControlParameter::SHOW_ISOTOPES));
    parameterChanged(ControlParameter::SHOW_EXPLICIT_HYDROGENS, view.getParameter(ControlParameter::SHOW_EXPLICIT_HYDROGENS));
    parameterChanged(ControlParameter::SHOW_HYDROGEN_COUNTS, view.getParameter(ControlParameter::SHOW_HYDROGEN_COUNTS));
    parameterChanged(ControlParameter::SHOW_NON_CARBON_HYDROGEN_COUNTS, view.getParameter(ControlParameter::SHOW_NON_CARBON_HYDROGEN_COUNTS));
    parameterChanged(ControlParameter::SHOW_ATOM_QUERY_INFOS, view.getParameter(ControlParameter::SHOW_ATOM_QUERY_INFOS));
    parameterChanged(ControlParameter::SHOW_ATOM_REACTION_INFOS, view.getParameter(ControlParameter::SHOW_ATOM_REACTION_INFOS));
    parameterChanged(ControlParameter::SHOW_RADICAL_ELECTRONS, view.getParameter(ControlParameter::SHOW_RADICAL_ELECTRONS));
    parameterChanged(ControlParameter::SHOW_ATOM_CONFIGURATION_LABELS, view.getParameter(ControlParameter::SHOW_ATOM_CONFIGURATION_LABELS));
    parameterChanged(ControlParameter::SHOW_ATOM_CUSTOM_LABELS, view.getParameter(ControlParameter::SHOW_ATOM_CUSTOM_LABELS));
    parameterChanged(ControlParameter::ENABLE_ATOM_HIGHLIGHTING, view.getParameter(ControlParameter::ENABLE_ATOM_HIGHLIGHTING));

    parameterChanged(ControlParameter::HIGHLIGHT_AREA_OUTLINE_WIDTH, view.getParameter(ControlParameter::HIGHLIGHT_AREA_OUTLINE_WIDTH));
    
    parameterChanged(ControlParameter::BOND_COLOR, view.getParameter(ControlParameter::BOND_COLOR));
    parameterChanged(ControlParameter::BOND_LINE_WIDTH, view.getParameter(ControlParameter::BOND_LINE_WIDTH));
    parameterChanged(ControlParameter::BOND_LINE_SPACING, view.getParameter(ControlParameter::BOND_LINE_SPACING));
    parameterChanged(ControlParameter::STEREO_BOND_WEDGE_WIDTH, view.getParameter(ControlParameter::STEREO_BOND_WEDGE_WIDTH));
    parameterChanged(ControlParameter::STEREO_BOND_HASH_SPACING, view.getParameter(ControlParameter::STEREO_BOND_HASH_SPACING));
    parameterChanged(ControlParameter::REACTION_CENTER_LINE_LENGTH, view.getParameter(ControlParameter::REACTION_CENTER_LINE_LENGTH));
    parameterChanged(ControlParameter::REACTION_CENTER_LINE_SPACING, view.getParameter(ControlParameter::REACTION_CENTER_LINE_SPACING));
    parameterChanged(ControlParameter::DOUBLE_BOND_TRIM_LENGTH, view.getParameter(ControlParameter::DOUBLE_BOND_TRIM_LENGTH));
    parameterChanged(ControlParameter::TRIPLE_BOND_TRIM_LENGTH, view.getParameter(ControlParameter::TRIPLE_BOND_TRIM_LENGTH));
    parameterChanged(ControlParameter::BOND_LABEL_FONT, view.getParameter(ControlParameter::BOND_LABEL_FONT));
    parameterChanged(ControlParameter::BOND_LABEL_SIZE, view.getParameter(ControlParameter::BOND_LABEL_SIZE));
    parameterChanged(ControlParameter::BOND_CONFIGURATION_LABEL_FONT, view.getParameter(ControlParameter::BOND_CONFIGURATION_LABEL_FONT));
    parameterChanged(ControlParameter::BOND_CONFIGURATION_LABEL_COLOR, view.getParameter(ControlParameter::BOND_CONFIGURATION_LABEL_COLOR));
    parameterChanged(ControlParameter::BOND_CONFIGURATION_LABEL_SIZE, view.getParameter(ControlParameter::BOND_CONFIGURATION_LABEL_SIZE));
    parameterChanged(ControlParameter::BOND_CUSTOM_LABEL_FONT, view.getParameter(ControlParameter::BOND_CUSTOM_LABEL_FONT));
    parameterChanged(ControlParameter::BOND_CUSTOM_LABEL_COLOR, view.getParameter(ControlParameter::BOND_CUSTOM_LABEL_COLOR));
    parameterChanged(ControlParameter::BOND_CUSTOM_LABEL_SIZE, view.getParameter(ControlParameter::BOND_CUSTOM_LABEL_SIZE));
    parameterChanged(ControlParameter::BOND_LABEL_MARGIN, view.getParameter(ControlParameter::BOND_LABEL_MARGIN));
    parameterChanged(ControlParameter::BOND_HIGHLIGHT_AREA_WIDTH, view.getParameter(ControlParameter::BOND_HIGHLIGHT_AREA_WIDTH));
    parameterChanged(ControlParameter::BOND_HIGHLIGHT_AREA_BRUSH, view.getParameter(ControlParameter::BOND_HIGHLIGHT_AREA_BRUSH));
    parameterChanged(ControlParameter::BOND_HIGHLIGHT_AREA_OUTLINE_PEN, view.getParameter(ControlParameter::BOND_HIGHLIGHT_AREA_OUTLINE_PEN));
    parameterChanged(ControlParameter::SHOW_BOND_REACTION_INFOS, view.getParameter(ControlParameter::SHOW_BOND_REACTION_INFOS));
    parameterChanged(ControlParameter::SHOW_BOND_QUERY_INFOS, view.getParameter(ControlParameter::SHOW_BOND_QUERY_INFOS));
    parameterChanged(ControlParameter::SHOW_STEREO_BONDS, view.getParameter(ControlParameter::SHOW_STEREO_BONDS));
    parameterChanged(ControlParameter::SHOW_BOND_CONFIGURATION_LABELS, view.getParameter(ControlParameter::SHOW_BOND_CONFIGURATION_LABELS));
    parameterChanged(ControlParameter::SHOW_BOND_CUSTOM_LABELS, view.getParameter(ControlParameter::SHOW_BOND_CUSTOM_LABELS));
    parameterChanged(ControlParameter::ENABLE_BOND_HIGHLIGHTING, view.getParameter(ControlParameter::ENABLE_BOND_HIGHLIGHTING));
}

void Vis::StructureView2DParameters::parameterChanged(const Base::LookupKey& key, Base::Any val)
{
    using namespace ControlParameterDefault;

    if (key == ControlParameter::VIEWPORT) {
        setViewport(val.isEmpty() ? VIEWPORT : val.getData<Rectangle2D>());
        return;
    }

    if (key == ControlParameter::SIZE_ADJUSTMENT) {
        setSizeAdjustment(val.isEmpty() ? SIZE_ADJUSTMENT : val.getData<unsigned int>());
        return;
    }

    if (key == ControlParameter::BOND_LENGTH) {
        setStdBondLength(val.isEmpty() ? BOND_LENGTH.getValue() : val.getData<SizeSpecification>().getValue());
        return;
    }

    if (key == ControlParameter::ALIGNMENT) {
        setAlignment(val.isEmpty() ? ALIGNMENT : val.getData<unsigned int>());
        return;
    }

    if (key == ControlParameter::BACKGROUND_BRUSH) {
        setBackgroundBrush(val.isEmpty() ? BACKGROUND_BRUSH : val.getData<Brush>());
        return;
    }

    if (key == ControlParameter::ATOM_COLOR_TABLE) {
        setAtomColorTable(val.isEmpty() ? ColorTable::SharedPointer() : val.getData<ColorTable::SharedPointer>());
        return;
    }

    if (key == ControlParameter::USE_CALCULATED_ATOM_COORDINATES) {
        useCalculatedAtomCoords(val.isEmpty() ? USE_CALCULATED_ATOM_COORDINATES : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::ATOM_COLOR) {
        setAtomColor(val.isEmpty() ? ATOM_COLOR : val.getData<Color>());
        return;
    }

    if (key == ControlParameter::ATOM_LABEL_FONT) {
        setAtomLabelFont(val.isEmpty() ? ATOM_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::ATOM_LABEL_SIZE) {
        setAtomLabelSize(val.isEmpty() ? ATOM_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::SECONDARY_ATOM_LABEL_FONT) {
        setSecondaryAtomLabelFont(val.isEmpty() ? SECONDARY_ATOM_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::SECONDARY_ATOM_LABEL_SIZE) {
        setSecondaryAtomLabelSize(val.isEmpty() ? SECONDARY_ATOM_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::ATOM_CONFIGURATION_LABEL_FONT) {
        setAtomConfigLabelFont(val.isEmpty() ? ATOM_CONFIGURATION_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::ATOM_CONFIGURATION_LABEL_COLOR) {
        setAtomConfigLabelColor(val.isEmpty() ? ATOM_CONFIGURATION_LABEL_COLOR : val.getData<Color>());
        return;
    }

    if (key == ControlParameter::ATOM_CONFIGURATION_LABEL_SIZE) {
        setAtomConfigLabelSize(val.isEmpty() ? ATOM_CONFIGURATION_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }
    
    if (key == ControlParameter::ATOM_CUSTOM_LABEL_FONT) {
        setAtomCustomLabelFont(val.isEmpty() ? ATOM_CUSTOM_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::ATOM_CUSTOM_LABEL_COLOR) {
        setAtomCustomLabelColor(val.isEmpty() ? ATOM_CUSTOM_LABEL_COLOR : val.getData<Color>());
        return;
    }

    if (key == ControlParameter::ATOM_CUSTOM_LABEL_SIZE) {
        setAtomCustomLabelSize(val.isEmpty() ? ATOM_CUSTOM_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }
    
    if (key == ControlParameter::ATOM_LABEL_MARGIN) {
        setAtomLabelMargin(val.isEmpty() ? ATOM_LABEL_MARGIN : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::RADICAL_ELECTRON_DOT_SIZE) {
        setRadicalElectronDotSize(val.isEmpty() ? RADICAL_ELECTRON_DOT_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::ATOM_HIGHLIGHT_AREA_SIZE) {
        setAtomHighlightAreaSize(val.isEmpty() ? ATOM_HIGHLIGHT_AREA_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::ATOM_HIGHLIGHT_AREA_BRUSH) {
        setAtomHighlightAreaBrush(val.isEmpty() ? ATOM_HIGHLIGHT_AREA_BRUSH : val.getData<Brush>());
        return;
    }

    if (key == ControlParameter::ATOM_HIGHLIGHT_AREA_OUTLINE_PEN) {
        setAtomHighlightAreaPen(val.isEmpty() ? ATOM_HIGHLIGHT_AREA_OUTLINE_PEN : val.getData<Pen>());
        return;
    }

    if (key == ControlParameter::BREAK_ATOM_HIGHLIGHT_AREA_OUTLINE) {
        breakAtomHighlightAreaOutline(val.isEmpty() ? BREAK_ATOM_HIGHLIGHT_AREA_OUTLINE : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_CARBONS) {
        showCarbons(val.isEmpty() ? SHOW_CARBONS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_CHARGES) {
        showCharges(val.isEmpty() ? SHOW_CHARGES : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_ISOTOPES) {
        showIsotopes(val.isEmpty() ? SHOW_ISOTOPES : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_EXPLICIT_HYDROGENS) {
        showExplicitHydrogens(val.isEmpty() ? SHOW_EXPLICIT_HYDROGENS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_HYDROGEN_COUNTS) {
        showHydrogenCounts(val.isEmpty() ? SHOW_HYDROGEN_COUNTS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_NON_CARBON_HYDROGEN_COUNTS) {
        showNonCarbonHydrogenCounts(val.isEmpty() ? SHOW_NON_CARBON_HYDROGEN_COUNTS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_ATOM_QUERY_INFOS) {
        showAtomQueryInfos(val.isEmpty() ? SHOW_ATOM_QUERY_INFOS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_ATOM_REACTION_INFOS) {
        showAtomReactionInfos(val.isEmpty() ? SHOW_ATOM_REACTION_INFOS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_RADICAL_ELECTRONS) {
        showRadicalElectrons(val.isEmpty() ? SHOW_RADICAL_ELECTRONS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_ATOM_CONFIGURATION_LABELS) {
        showAtomConfigLabels(val.isEmpty() ? SHOW_ATOM_CONFIGURATION_LABELS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_ATOM_CUSTOM_LABELS) {
        showAtomCustomLabels(val.isEmpty() ? SHOW_ATOM_CUSTOM_LABELS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::ENABLE_ATOM_HIGHLIGHTING) {
        enableAtomHighlighting(val.isEmpty() ? ENABLE_ATOM_HIGHLIGHTING : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::HIGHLIGHT_AREA_OUTLINE_WIDTH) {
        setHighlightAreaOutlineWidth(val.isEmpty() ? HIGHLIGHT_AREA_OUTLINE_WIDTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_COLOR) {
        setBondColor(val.isEmpty() ? BOND_COLOR : val.getData<Color>());
        return;
    }

    if (key == ControlParameter::BOND_LINE_WIDTH) {
        setBondLineWidth(val.isEmpty() ? BOND_LINE_WIDTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_LINE_SPACING) {
        setBondLineSpacing(val.isEmpty() ? BOND_LINE_SPACING : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::STEREO_BOND_WEDGE_WIDTH) {
        setStereoBondWedgeWidth(val.isEmpty() ? STEREO_BOND_WEDGE_WIDTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::STEREO_BOND_HASH_SPACING) {
        setStereoBondHashSpacing(val.isEmpty() ? STEREO_BOND_HASH_SPACING : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::REACTION_CENTER_LINE_LENGTH) {
        setReactionCenterLineLength(val.isEmpty() ? REACTION_CENTER_LINE_LENGTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::REACTION_CENTER_LINE_SPACING) {
        setReactionCenterLineSpacing(val.isEmpty() ? REACTION_CENTER_LINE_SPACING : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::DOUBLE_BOND_TRIM_LENGTH) {
        setDoubleBondTrimLength(val.isEmpty() ? DOUBLE_BOND_TRIM_LENGTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::TRIPLE_BOND_TRIM_LENGTH) {
        setTripleBondTrimLength(val.isEmpty() ? TRIPLE_BOND_TRIM_LENGTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_LABEL_FONT) {
        setBondLabelFont(val.isEmpty() ? BOND_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::BOND_LABEL_SIZE) {
        setBondLabelSize(val.isEmpty() ? BOND_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_CONFIGURATION_LABEL_FONT) {
        setBondConfigLabelFont(val.isEmpty() ? BOND_CONFIGURATION_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::BOND_CONFIGURATION_LABEL_COLOR) {
        setBondConfigLabelColor(val.isEmpty() ? BOND_CONFIGURATION_LABEL_COLOR : val.getData<Color>());
        return;
    }

    if (key == ControlParameter::BOND_CONFIGURATION_LABEL_SIZE) {
        setBondConfigLabelSize(val.isEmpty() ? BOND_CONFIGURATION_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_CUSTOM_LABEL_FONT) {
        setBondCustomLabelFont(val.isEmpty() ? BOND_CUSTOM_LABEL_FONT : val.getData<Font>());
        return;
    }

    if (key == ControlParameter::BOND_CUSTOM_LABEL_COLOR) {
        setBondCustomLabelColor(val.isEmpty() ? BOND_CUSTOM_LABEL_COLOR : val.getData<Color>());
        return;
    }

    if (key == ControlParameter::BOND_CUSTOM_LABEL_SIZE) {
        setBondCustomLabelSize(val.isEmpty() ? BOND_CUSTOM_LABEL_SIZE : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_LABEL_MARGIN) {
        setBondLabelMargin(val.isEmpty() ? BOND_LABEL_MARGIN : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_HIGHLIGHT_AREA_WIDTH) {
        setBondHighlightAreaWidth(val.isEmpty() ? BOND_HIGHLIGHT_AREA_WIDTH : val.getData<SizeSpecification>());
        return;
    }

    if (key == ControlParameter::BOND_HIGHLIGHT_AREA_BRUSH) {
        setBondHighlightAreaBrush(val.isEmpty() ? BOND_HIGHLIGHT_AREA_BRUSH : val.getData<Brush>());
        return;
    }

    if (key == ControlParameter::BOND_HIGHLIGHT_AREA_OUTLINE_PEN) {
        setBondHighlightAreaPen(val.isEmpty() ? BOND_HIGHLIGHT_AREA_OUTLINE_PEN : val.getData<Pen>());
        return;
    }
    
    if (key == ControlParameter::SHOW_BOND_REACTION_INFOS) {
        showBondReactionInfos(val.isEmpty() ? SHOW_BOND_REACTION_INFOS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_BOND_QUERY_INFOS) {
        showBondQueryInfos(val.isEmpty() ? SHOW_BOND_QUERY_INFOS : val.getData<bool>());
        return;
    }

    if (key == ControlParameter::SHOW_STEREO_BONDS) {
        showStereoBonds(val.isEmpty() ? SHOW_STEREO_BONDS : val.getData<bool>());
        return;
    }
    
    if (key == ControlParameter::SHOW_BOND_CONFIGURATION_LABELS) {
        showBondConfigLabels(val.isEmpty() ? SHOW_BOND_CONFIGURATION_LABELS : val.getData<bool>());
        return;
    }
    
    if (key == ControlParameter::SHOW_BOND_CUSTOM_LABELS) {
        showBondCustomLabels(val.isEmpty() ? SHOW_BOND_CUSTOM_LABELS : val.getData<bool>());
        return;
    }
    
    if (key == ControlParameter::ENABLE_BOND_HIGHLIGHTING)
        enableBondHighlighting(val.isEmpty() ? ENABLE_BOND_HIGHLIGHTING : val.getData<bool>());
}

void Vis::StructureView2DParameters::parameterRemoved(const Base::LookupKey& key)
{
    parameterChanged(key, view.getParameter(key));
}

void Vis::StructureView2DParameters::setViewport(const Rectangle2D& vp)
{
    if (viewport != vp) {
        viewport = vp;
        viewportChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAlignment(unsigned int align)
{
    if (alignment != align) {
        alignment = align;
        alignmentChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setStdBondLength(double length)
{
    if (stdBondLength != length) {
        stdBondLength = length;
        stdBondLengthChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setSizeAdjustment(unsigned int adjustment)
{
    if (sizeAdjustment != adjustment) {
        sizeAdjustment = adjustment;
        sizeAdjustmentChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBackgroundBrush(const Brush& brush)
{
    backgroundBrush = brush;
}

void Vis::StructureView2DParameters::setAtomColorTable(const ColorTable::SharedPointer& table_ptr)
{
    atomColorTable = table_ptr;
    graphicsAttributeChangedFlag = true;
}

void Vis::StructureView2DParameters::useCalculatedAtomCoords(bool use_calc_coords)
{
    if (useCalcAtomCoordsFlag != use_calc_coords) {
        useCalcAtomCoordsFlag = use_calc_coords;
        coordinatesChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomColor(const Color& color)
{
    if (atomColor != color) {
        atomColor = color;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomConfigLabelColor(const Color& color)
{
    if (atomConfigLabelColor != color) {
        atomConfigLabelColor = color;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomCustomLabelColor(const Color& color)
{
    if (atomCustomLabelColor != color) {
        atomCustomLabelColor = color;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomLabelFont(const Font& font)
{
    if (atomLabelFont != font) {
        atomLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setSecondaryAtomLabelFont(const Font& font)
{
    if (secondaryAtomLabelFont != font) {
        secondaryAtomLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomConfigLabelFont(const Font& font)
{
    if (atomConfigLabelFont != font) {
        atomConfigLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomCustomLabelFont(const Font& font)
{
    if (atomCustomLabelFont != font) {
        atomCustomLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomLabelSize(const SizeSpecification& size)
{
    if (atomLabelSize != size) {
        atomLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setSecondaryAtomLabelSize(const SizeSpecification& size)
{
    if (secondaryAtomLabelSize != size) {
        secondaryAtomLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomConfigLabelSize(const SizeSpecification& size)
{
    if (atomConfigLabelSize != size) {
        atomConfigLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomCustomLabelSize(const SizeSpecification& size)
{
    if (atomCustomLabelSize != size) {
        atomCustomLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomLabelMargin(const SizeSpecification& margin)
{
    if (atomLabelMargin != margin) {
        atomLabelMargin = margin;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setRadicalElectronDotSize(const SizeSpecification& size)
{
    if (radicalElectronDotSize != size) {
        radicalElectronDotSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomHighlightAreaSize(const SizeSpecification& size)
{
    if (atomHighlightAreaSize != size) {
        atomHighlightAreaSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomHighlightAreaBrush(const Brush& brush)
{
    if (atomHighlightAreaBrush != brush) {
        atomHighlightAreaBrush = brush;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setAtomHighlightAreaPen(const Pen& pen)
{
    if (atomHighlightAreaPen != pen) {
        atomHighlightAreaPen = pen;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::breakAtomHighlightAreaOutline(bool brk)
{
    if (breakAtomHighltAreaOutline != brk) {
        breakAtomHighltAreaOutline = brk;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showCarbons(bool show)
{
    if (showCarbonsFlag != show) {
        showCarbonsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showIsotopes(bool show)
{
    if (showIsotopesFlag != show) {
        showIsotopesFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showCharges(bool show)
{
    if (showChargesFlag != show) {
        showChargesFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showExplicitHydrogens(bool show)
{
    if (showExplicitHsFlag != show) {
        showExplicitHsFlag = show;
        explicitHVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showHydrogenCounts(bool show)
{
    if (showHydrogenCountsFlag != show) {
        showHydrogenCountsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showNonCarbonHydrogenCounts(bool show)
{
    if (showNonCarbonHydrogenCountsFlag != show) {
        showNonCarbonHydrogenCountsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showAtomReactionInfos(bool show)
{
    if (showAtomReactionInfosFlag != show) {
        showAtomReactionInfosFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showAtomQueryInfos(bool show)
{
    if (showAtomQueryInfosFlag != show) {
        showAtomQueryInfosFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showRadicalElectrons(bool show)
{
    if (showRadicalElectronsFlag != show) {
        showRadicalElectronsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showAtomConfigLabels(bool show)
{
    if (showAtomConfigLabelsFlag != show) {
        showAtomConfigLabelsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showAtomCustomLabels(bool show)
{
    if (showAtomCustomLabelsFlag != show) {
        showAtomCustomLabelsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::enableAtomHighlighting(bool enable)
{
    if (enableAtomHighlightingFlag != enable) {
        enableAtomHighlightingFlag = enable;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setHighlightAreaOutlineWidth(const SizeSpecification& width)
{
    if (highlightAreaOutlineWidth != width) {
        highlightAreaOutlineWidth = width;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondColor(const Color& color)
{
    if (bondColor != color) {
        bondColor = color;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondLabelFont(const Font& font)
{
    if (bondLabelFont != font) {
        bondLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondLabelSize(const SizeSpecification& size)
{
    if (bondLabelSize != size) {
        bondLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondConfigLabelFont(const Font& font)
{
    if (bondConfigLabelFont != font) {
        bondConfigLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondConfigLabelColor(const Color& color)
{
    if (bondConfigLabelColor != color) {
        bondConfigLabelColor = color;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondConfigLabelSize(const SizeSpecification& size)
{
    if (bondConfigLabelSize != size) {
        bondConfigLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondCustomLabelFont(const Font& font)
{
    if (bondCustomLabelFont != font) {
        bondCustomLabelFont = font;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondCustomLabelColor(const Color& color)
{
    if (bondCustomLabelColor != color) {
        bondCustomLabelColor = color;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondCustomLabelSize(const SizeSpecification& size)
{
    if (bondCustomLabelSize != size) {
        bondCustomLabelSize = size;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondLabelMargin(const SizeSpecification& margin)
{
    if (bondLabelMargin != margin) {
        bondLabelMargin = margin;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondLineWidth(const SizeSpecification& width)
{
    if (bondLineWidth != width) {
        bondLineWidth = width;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondLineSpacing(const SizeSpecification& spacing)
{
    if (bondLineSpacing != spacing) {
        bondLineSpacing = spacing;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setStereoBondWedgeWidth(const SizeSpecification& width)
{
    if (stereoBondWedgeWidth != width) {
        stereoBondWedgeWidth = width;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setStereoBondHashSpacing(const SizeSpecification& dist)
{
    if (stereoBondHashSpacing != dist) {
        stereoBondHashSpacing = dist;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setReactionCenterLineLength(const SizeSpecification& length)
{
    if (reactionCenterLineLength != length) {
        reactionCenterLineLength = length;
        graphicsAttributeChangedFlag = true;
    }    
}

void Vis::StructureView2DParameters::setReactionCenterLineSpacing(const SizeSpecification& spacing)
{
    if (reactionCenterLineSpacing != spacing) {
        reactionCenterLineSpacing = spacing;
        graphicsAttributeChangedFlag = true;
    }    
}

void Vis::StructureView2DParameters::setDoubleBondTrimLength(const SizeSpecification& length)
{
    if (doubleBondTrimLength != length) {
        doubleBondTrimLength = length;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setTripleBondTrimLength(const SizeSpecification& length)
{
    if (tripleBondTrimLength != length) {
        tripleBondTrimLength = length;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondHighlightAreaWidth(const SizeSpecification& width)
{
    if (bondHighlightAreaWidth != width) {
        bondHighlightAreaWidth = width;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondHighlightAreaBrush(const Brush& brush)
{
    if (bondHighlightAreaBrush != brush) {
        bondHighlightAreaBrush = brush;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::setBondHighlightAreaPen(const Pen& pen)
{
    if (bondHighlightAreaPen != pen) {
        bondHighlightAreaPen = pen;
        graphicsAttributeChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showBondReactionInfos(bool show)
{
    if (showBondReactionInfosFlag != show) {
        showBondReactionInfosFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showBondQueryInfos(bool show)
{
    if (showBondQueryInfosFlag != show) {
        showBondQueryInfosFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showStereoBonds(bool show)
{
    if (showStereoBondsFlag != show) {
        showStereoBondsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showBondConfigLabels(bool show)
{
    if (showBondConfigLabelsFlag != show) {
        showBondConfigLabelsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::showBondCustomLabels(bool show)
{
    if (showBondCustomLabelsFlag != show) {
        showBondCustomLabelsFlag = show;
        propertyVisibilityChangedFlag = true;
    }
}

void Vis::StructureView2DParameters::enableBondHighlighting(bool enable)
{
    if (enableBondHighlightingFlag != enable) {
        enableBondHighlightingFlag = enable;
        propertyVisibilityChangedFlag = true;
    }
}
