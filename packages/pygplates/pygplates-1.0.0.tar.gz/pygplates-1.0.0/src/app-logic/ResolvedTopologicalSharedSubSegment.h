/* $Id$ */

/**
 * \file 
 * $Revision$
 * $Date$
 * 
 * Copyright (C) 2014 The University of Sydney, Australia
 *
 * This file is part of GPlates.
 *
 * GPlates is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License, version 2, as published by
 * the Free Software Foundation.
 *
 * GPlates is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

#ifndef GPLATES_APP_LOGIC_RESOLVEDTOPOLOGICALSHAREDSUBSEGMENT_H
#define GPLATES_APP_LOGIC_RESOLVEDTOPOLOGICALSHAREDSUBSEGMENT_H

#include <vector>
#include <boost/optional.hpp>

#include "ReconstructionGeometry.h"
#include "ResolvedSubSegmentRangeInSection.h"
#include "ResolvedTopologicalGeometrySubSegment.h"
#include "ResolvedVertexSourceInfo.h"
#include "VelocityDeltaTime.h"
#include "VelocityUnits.h"

#include "maths/GeometryOnSphere.h"
#include "maths/PointOnSphere.h"
#include "maths/PolylineOnSphere.h"
#include "maths/Vector3D.h"

#include "model/FeatureHandle.h"

#include "utils/Earth.h"
#include "utils/ReferenceCount.h"


namespace GPlatesAppLogic
{
	/**
	 * Associates a sub-segment (of a resolved topological section) with those resolved topologies
	 * (@a ResolvedTopologicalBoundary and @a ResolvedTopologicalNetwork) that share it as part of their boundary.
	 *
	 * This is kept as a separate class from @a ResolvedTopologicalGeometrySubSegment partly in order
	 * to avoid memory islands (cyclic references of shared pointers) - see below for more details -
	 * and partly for design reasons.
	 */
	class ResolvedTopologicalSharedSubSegment :
			public GPlatesUtils::ReferenceCount<ResolvedTopologicalSharedSubSegment>
	{
	public:

		typedef GPlatesUtils::non_null_intrusive_ptr<ResolvedTopologicalSharedSubSegment> non_null_ptr_type;
		typedef GPlatesUtils::non_null_intrusive_ptr<const ResolvedTopologicalSharedSubSegment> non_null_ptr_to_const_type;


		/**
		 * A resolved topology's relationship to the shared sub-segment.
		 */
		struct ResolvedTopologyInfo
		{
			ResolvedTopologyInfo(
					const ReconstructionGeometry::non_null_ptr_to_const_type &resolved_topology_,
					bool is_sub_segment_geometry_reversed_) :
				resolved_topology(resolved_topology_),
				is_sub_segment_geometry_reversed(is_sub_segment_geometry_reversed_)
			{  }

			/**
			 * Returns true if the resolved topology is on the *left* of the boundary sub-segment.
			 */
			bool
			is_resolved_topology_on_left() const;

			/**
			 * A resolved topology can be a @a ResolvedTopologicalBoundary (the boundary of a plate polygon)
			 * or a @a ResolvedTopologicalNetwork (the boundary of a deforming network).
			 */
			ReconstructionGeometry::non_null_ptr_to_const_type resolved_topology;

			// Is sub-segment geometry reversed with respect to the section geometry.
			bool is_sub_segment_geometry_reversed;
		};


		static
		non_null_ptr_type
		create(
				const ResolvedSubSegmentRangeInSection &shared_sub_segment,
				const std::vector<ResolvedTopologyInfo> &sharing_resolved_topologies,
				const GPlatesModel::FeatureHandle::const_weak_ref &shared_segment_feature_ref,
				const ReconstructionGeometry::non_null_ptr_to_const_type &shared_segment_reconstruction_geometry)
		{
			return non_null_ptr_type(
					new ResolvedTopologicalSharedSubSegment(
							shared_sub_segment,
							sharing_resolved_topologies,
							shared_segment_feature_ref,
							shared_segment_reconstruction_geometry));
		}


		//! Reference to the feature referenced by the topological section.
		const GPlatesModel::FeatureHandle::const_weak_ref &
		get_feature_ref() const
		{
			return d_shared_segment_feature_ref;
		}

		/**
		 * The reconstruction geometry that this shared sub-segment was obtained from.
		 *
		 * This can be either a reconstructed feature geometry or a resolved topological *line*.
		 */
		const ReconstructionGeometry::non_null_ptr_to_const_type &
		get_reconstruction_geometry() const
		{
			return d_shared_segment_reconstruction_geometry;
		}

		/**
		 * Returns the full (un-clipped) section geometry.
		 *
		 * It will be a point, multi-point or polyline (a polygon exterior ring is converted to polyline).
		 */
		GPlatesMaths::GeometryOnSphere::non_null_ptr_to_const_type
		get_section_geometry() const
		{
			return d_shared_sub_segment.get_section_geometry();
		}

		/**
		 * The shared sub-segment range with the entire topological section geometry.
		 */
		const ResolvedSubSegmentRangeInSection &
		get_shared_sub_segment() const
		{
			return d_shared_sub_segment;
		}

		/**
		 * Returns the resolved topologies that share this sub-segment.
		 *
		 * Along with each resolved topology there is also returned a flag to indicated whether the
		 * shared sub-segment geometry (returned by @a get_shared_sub_segment_geometry) had its points
		 * reversed in order before contributing to that particular resolved topology.
		 *
		 * Resolved topologies can be @a ResolvedTopologicalBoundary (the boundary of a plate polygon)
		 * and @a ResolvedTopologicalNetwork (the boundary of a deforming network).
		 * For example the sub-segment at the boundary of a deforming @a ResolvedTopologicalNetwork
		 * is also shared by a non-deforming @a ResolvedTopologicalBoundary (plate polygon).
		 *
		 * Typically there will be two sharing boundaries but there can be one if a topological
		 * boundary has no adjacent boundary (eg, topologies don't cover the entire globe).
		 * If there are more than two sharing boundaries then there is probably some overlap of
		 * topologies occurring.
		 */
		const std::vector<ResolvedTopologyInfo> &
		get_sharing_resolved_topologies() const
		{
			return d_sharing_resolved_topologies;
		}

		/**
		 * The subset of vertices of topological section used in the sharing resolved topologies.
		 *
		 * Note that this includes rubber band points (if any) in the returned polyline, otherwise
		 * it would be possible to have no geometry points (and hence no returned polyline).
		 *
		 * NOTE: These are the un-reversed vertices of the original geometry that contributed this
		 *       shared sub-segment - the actual order of vertices (as contributed to each sharing resolved
		 *       topological geometries along with other sub-segments) depends on the specific sharing resolved
		 *       topology (different topologies will have different reverse flags - see @a ResolvedTopologyInfo).
		 */
		GPlatesMaths::PolylineOnSphere::non_null_ptr_to_const_type
		get_shared_sub_segment_geometry() const
		{
			return d_shared_sub_segment.get_geometry();
		}

		/**
		 * Returns the points in the sub-segment geometry returned by @a get_shared_sub_segment_geometry.
		 */
		void
		get_shared_sub_segment_geometry_points(
				std::vector<GPlatesMaths::PointOnSphere> &geometry_points) const
		{
			get_shared_sub_segment_points(geometry_points, true/*include_rubber_band_points*/);
		}

		/**
		 * Returns the velocities at the points returned by @a get_shared_sub_segment_geometry_points.
		 *
		 * Note: Each velocity maps to a point in @a get_shared_sub_segment_geometry_points.
		 *
		 * Note: The number of velocities is guaranteed to match points in @a get_shared_sub_segment_geometry_points.
		 */
		void
		get_shared_sub_segment_geometry_point_velocities(
				std::vector<GPlatesMaths::Vector3D> &geometry_point_velocities,
				const double &velocity_delta_time = 1.0,
				VelocityDeltaTime::Type velocity_delta_time_type = VelocityDeltaTime::T_PLUS_DELTA_T_TO_T,
				VelocityUnits::Value velocity_units = VelocityUnits::CMS_PER_YR,
				const double &earth_radius_in_kms = GPlatesUtils::Earth::EQUATORIAL_RADIUS_KMS) const
		{
			get_shared_sub_segment_point_velocities(
					geometry_point_velocities,
					true/*include_rubber_band_points*/,
					velocity_delta_time,
					velocity_delta_time_type,
					velocity_units,
					earth_radius_in_kms);
		}

		/**
		 * Returns the shared per-point source infos at the points returned by @a get_shared_sub_segment_geometry_points.
		 *
		 * Note: Each source info maps to a point in @a get_shared_sub_segment_geometry_points.
		 *
		 * Note: The number of source infos is guaranteed to match points in @a get_shared_sub_segment_geometry_points.
		 */
		void
		get_shared_sub_segment_geometry_point_source_infos(
				resolved_vertex_source_info_seq_type &point_source_infos) const
		{
			get_shared_sub_segment_point_source_infos(point_source_infos, true/*include_rubber_band_points*/);
		}

		/**
		 * Returns the shared per-point source features at the points returned by @a get_shared_sub_segment_geometry_points.
		 *
		 * Note: Each source feature maps to a point in @a get_shared_sub_segment_geometry_points.
		 *
		 * Note: The number of source features is guaranteed to match points in @a get_shared_sub_segment_geometry_points.
		 */
		void
		get_shared_sub_segment_geometry_point_source_features(
				std::vector<GPlatesModel::FeatureHandle::weak_ref> &point_source_features) const
		{
			get_shared_sub_segment_point_source_features(point_source_features, true/*include_rubber_band_points*/);
		}


		/**
		 * Returns the (unreversed) shared sub-segment points.
		 *
		 * Does not clear @a geometry_points - just appends points.
		 *
		 * NOTE: These are the un-reversed vertices of the original geometry that contributed this
		 *       shared sub-segment - the actual order of vertices (as contributed to each sharing resolved
		 *       topological geometries along with other sub-segments) depends on the specific sharing resolved
		 *       topology (different topologies will have different reverse flags - see @a ResolvedTopologyInfo).
		 */
		void
		get_shared_sub_segment_points(
				std::vector<GPlatesMaths::PointOnSphere> &geometry_points,
				bool include_rubber_band_points = true) const
		{
			d_shared_sub_segment.get_geometry_points(geometry_points, include_rubber_band_points);
		}

		/**
		 * Returns the shared sub-segment points as they contribute to a specific sharing resolved topology.
		 *
		 * The @a use_reverse flag should be associated with the desired sharing resolved topology.
		 * For example, it can be obtained from the relevant @a ResolvedTopologyInfo.
		 *
		 * These points are @a get_shared_sub_segment_points if @a use_reverse is false,
		 * otherwise they are a reversed version of @a get_shared_sub_segment_points.
		 *
		 * Does not clear @a geometry_points - just appends points.
		 */
		void
		get_reversed_shared_sub_segment_points(
				std::vector<GPlatesMaths::PointOnSphere> &geometry_points,
				bool use_reverse,
				bool include_rubber_band_points = true) const
		{
			d_shared_sub_segment.get_reversed_geometry_points(geometry_points, use_reverse, include_rubber_band_points);
		}


		/**
		 * Returns the velocities at the (unreversed) shared sub-segment points.
		 *
		 * Note: Each velocity maps to a point in @a get_shared_sub_segment_points.
		 *
		 * Note: The number of velocities is guaranteed to match points in @a get_shared_sub_segment_points
		 *       (with the same value of @a include_rubber_band_points).
		 */
		void
		get_shared_sub_segment_point_velocities(
				std::vector<GPlatesMaths::Vector3D> &geometry_point_velocities,
				bool include_rubber_band_points = true,
				const double &velocity_delta_time = 1.0,
				VelocityDeltaTime::Type velocity_delta_time_type = VelocityDeltaTime::T_PLUS_DELTA_T_TO_T,
				VelocityUnits::Value velocity_units = VelocityUnits::CMS_PER_YR,
				const double &earth_radius_in_kms = GPlatesUtils::Earth::EQUATORIAL_RADIUS_KMS) const;

		/**
		 * Returns the velocities at the shared sub-segment points as they contribute to a specific sharing resolved topology.
		 *
		 * Note: Each velocity maps to a point in @a get_reversed_shared_sub_segment_points.
		 *
		 * Note: The number of velocities is guaranteed to match points in @a get_reveget_reversed_shared_sub_segment_pointsrsed_sub_segment_points
		 *       (with the same values of @a use_reverse and @a include_rubber_band_points).
		 */
		void
		get_reversed_shared_sub_segment_point_velocities(
				std::vector<GPlatesMaths::Vector3D> &geometry_point_velocities,
				bool use_reverse,
				bool include_rubber_band_points = true,
				const double &velocity_delta_time = 1.0,
				VelocityDeltaTime::Type velocity_delta_time_type = VelocityDeltaTime::T_PLUS_DELTA_T_TO_T,
				VelocityUnits::Value velocity_units = VelocityUnits::CMS_PER_YR,
				const double &earth_radius_in_kms = GPlatesUtils::Earth::EQUATORIAL_RADIUS_KMS) const;


		/**
		 * Returns the (unreversed) shared per-point source reconstructed feature geometries.
		 *
		 * Each point in @a get_shared_sub_segment_points references a source reconstructed feature geometry.
		 * This method returns the same number of point sources as points returned by @a get_shared_sub_segment_points.
		 *
		 * Does not clear @a point_source_infos - just appends point sources.
		 *
		 * @throws PreconditionViolationError if the section reconstruction geometry passed into @a create
		 * is neither a @a ReconstructedFeatureGeometry nor a @a ResolvedTopologicalLine.
		 */
		void
		get_shared_sub_segment_point_source_infos(
				resolved_vertex_source_info_seq_type &point_source_infos,
				bool include_rubber_band_points = true) const;

		/**
		 * Same as @a get_shared_sub_segment_point_source_infos but reverses them if necessary such that
		 * they are in the same order as @a get_reversed_shared_sub_segment_points.
		 *
		 * The @a use_reverse flag should be associated with the desired sharing resolved topology.
		 * For example, it can be obtained from the relevant @a ResolvedTopologyInfo.
		 *
		 * These are @a get_shared_sub_segment_point_source_infos if @a use_reverse is false,
		 * otherwise they are a reversed version of @a get_shared_sub_segment_point_source_infos.
		 */
		void
		get_reversed_shared_sub_segment_point_source_infos(
				resolved_vertex_source_info_seq_type &point_source_infos,
				bool use_reverse,
				bool include_rubber_band_points = true) const;


		/**
		 * Returns the (unreversed) shared per-point source features.
		 *
		 * Each point in @a get_shared_sub_segment_points references a source feature.
		 * This method returns the same number of point source features as points returned by @a get_shared_sub_segment_points.
		 *
		 * Does not clear @a point_source_features - just appends point source features.
		 *
		 * @throws PreconditionViolationError if the section reconstruction geometry passed into @a create
		 * is neither a @a ReconstructedFeatureGeometry nor a @a ResolvedTopologicalLine.
		 */
		void
		get_shared_sub_segment_point_source_features(
				std::vector<GPlatesModel::FeatureHandle::weak_ref> &point_source_features,
				bool include_rubber_band_points = true) const;

		/**
		 * Same as @a get_shared_sub_segment_point_source_features but reverses them if necessary such that
		 * they are in the same order as @a get_reversed_shared_sub_segment_points.
		 *
		 * The @a use_reverse flag should be associated with the desired sharing resolved topology.
		 * For example, it can be obtained from the relevant @a ResolvedTopologyInfo.
		 *
		 * These are @a get_shared_sub_segment_point_source_features if @a use_reverse is false,
		 * otherwise they are a reversed version of @a get_shared_sub_segment_point_source_features.
		 */
		void
		get_reversed_shared_sub_segment_point_source_features(
				std::vector<GPlatesModel::FeatureHandle::weak_ref> &point_source_features,
				bool use_reverse,
				bool include_rubber_band_points = true) const;


		/**
		* Return any sub-segments of the resolved topological section that this sub-segment came from.
		*
		* If topological section is a ResolvedTopologicalLine then returns sub-segments, otherwise returns none.
		*
		* If this sub-segment came from a ResolvedTopologicalLine then it will have its own sub-segments, otherwise
		* if from a ReconstructedFeatureGeometry then there will be no sub-segments.
		*
		* Some, or all, of those sub-segments (belong to the ResolvedTopologicalLine) will contribute to this sub-segment.
		* And part, or all, of the first and last contributing sub-segments will contribute to this sub-segment
		* (due to intersection/clipping).
		*
		* NOTE: These are not *shared* sub-segments. They simply represent the child sub-segments that contribute
		* to this shared parent sub-segment (part of resolved topological line).
		* The information of which topologies share the parent sub-segment, and hence its child sub-sub-segments,
		* still comes from @a get_sharing_resolved_topologies.
		*
		* Note: Each child sub-sub-segment also has its own reverse flag (whether it was reversed when contributing
		* to parent sub-segment), and the parent sub-segment also has a reverse flag for each topology that shares it
		* (which determines whether parent sub-segment was reversed when contributing to that topology).
		* So to determine whether a child sub-sub-segment was effectively reversed when contributing to a particular final
		* topology depends on both reverse flags (the child sub-sub-segment and parent sub-segment reverse flags).
		*/
		const boost::optional<sub_segment_seq_type> &
		get_sub_sub_segments() const;

	private:

		//! The shared sub-segment.
		ResolvedSubSegmentRangeInSection d_shared_sub_segment;

		/**
		 * The resolved topologies that share this sub-segment.
		 *
		 * NOTE: We won't get a memory island (cyclic reference of shared pointers) because
		 * @a ResolvedTopologicalSharedSubSegment are not owned by
		 * @a ResolvedTopologicalBoundary and @a ResolvedTopologicalNetwork
		 * (only @a ResolvedTopologicalGeometrySubSegment are owned by them).
		 */
		std::vector<ResolvedTopologyInfo> d_sharing_resolved_topologies;

		//! Reference to the source feature handle of the topological section.
		GPlatesModel::FeatureHandle::const_weak_ref d_shared_segment_feature_ref;

		/**
		 * The shared segment reconstruction geometry.
		 *
		 * This is either a reconstructed feature geometry or a resolved topological *line*.
		 */
		ReconstructionGeometry::non_null_ptr_to_const_type d_shared_segment_reconstruction_geometry;


		/**
		 * Each point in the shared subsegment geometry can potentially reference a different
		 * source reconstructed feature geometry.
		 *
		 * Note: All points can share the same point source info (if this subsegment came from a
		 * reconstructed feature geometry), but there is still one pointer for each point.
		 * However this does not use much extra memory, 8 bytes per point compared to the
		 * 32 bytes per PointOnSphere in the geometry.
		 *
		 * As an optimisation, this is only created when first requested.
		 */
		mutable boost::optional<resolved_vertex_source_info_seq_type> d_point_source_infos;

		/**
		 * Each point in the shared subsegment geometry can potentially reference a different source feature.
		 *
		 * As an optimisation, this is only created when first requested.
		 */
		mutable boost::optional<std::vector<GPlatesModel::FeatureHandle::weak_ref>> d_point_source_features;

		/**
		* Sub-segments of our ResolvedTopologicalLine topological section (if one) than contribute to this shared sub-segment.
		*/
		mutable boost::optional< std::vector<ResolvedTopologicalGeometrySubSegment::non_null_ptr_type> > d_sub_sub_segments;
		mutable bool d_calculated_sub_sub_segments;


		ResolvedTopologicalSharedSubSegment(
				const ResolvedSubSegmentRangeInSection &shared_sub_segment,
				const std::vector<ResolvedTopologyInfo> &sharing_resolved_topologies,
				const GPlatesModel::FeatureHandle::const_weak_ref &shared_segment_feature_ref,
				const ReconstructionGeometry::non_null_ptr_to_const_type &shared_segment_reconstruction_geometry) :
			d_shared_sub_segment(shared_sub_segment),
			d_sharing_resolved_topologies(sharing_resolved_topologies),
			d_shared_segment_feature_ref(shared_segment_feature_ref),
			d_shared_segment_reconstruction_geometry(shared_segment_reconstruction_geometry),
			d_calculated_sub_sub_segments(false)
		{  }
	};


	//! Typedef for a sequence of @a ResolvedTopologicalSharedSubSegment objects.
	typedef std::vector<ResolvedTopologicalSharedSubSegment::non_null_ptr_type> shared_sub_segment_seq_type;
}

#endif // GPLATES_APP_LOGIC_RESOLVEDTOPOLOGICALSHAREDSUBSEGMENT_H
