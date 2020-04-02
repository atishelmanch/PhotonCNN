#include "flashgg/DataFormats/interface/SinglePhotonView.h"

namespace flashgg {

    bool SinglePhotonView::MakePhoton() const
    {
        if( hasPhoton_ ) {
            return false;
        } else if( hasVtx_ ) {
            float vtx_X = vtxRef_->x();
            float vtx_Y = vtxRef_->y();
            float vtx_Z = vtxRef_->z();

            float sc_X = phoPtr_->superCluster()->x();
            float sc_Y = phoPtr_->superCluster()->y();
            float sc_Z = phoPtr_->superCluster()->z();

            math::XYZVector vtx_Pos( vtx_X, vtx_Y, vtx_Z );
            math::XYZVector sc_Pos( sc_X, sc_Y, sc_Z );

            math::XYZVector direction = sc_Pos - vtx_Pos;
            math::XYZVector p = ( direction.Unit() ) * ( phoPtr_->energy() );
            math::XYZTLorentzVector corrected_p4( p.x(), p.y(), p.z(), phoPtr_->energy() );

            pho_ =  flashgg::Photon( *phoPtr_ );
            pho_.setP4( corrected_p4 );
            hasPhoton_ = true;
        } else {
            pho_ = flashgg::Photon( *phoPtr_ );
            hasPhoton_ = true;
        }
        return true;
    }


    void SinglePhotonView::MakePersistent()
    {
        if( !persistVec_.size() ) {
            MakePhoton();
            pho_.embedSuperCluster();
            persistVec_.push_back( pho_ );
        }
    }

    const Photon *SinglePhotonView::photon() const
    {
        if( persistVec_.size() ) {
            return &persistVec_[0];
        } else {
            MakePhoton();
            return &pho_;
        }
    }

    Photon &SinglePhotonView::getPhoton()
    {
        if( !persistVec_.size() ) {
            throw cms::Exception( "IncorrectUsage" ) << "SinglePhotonView not persistified. If you really want a non-const photon, call MakePersistent()";
        }
        return persistVec_[0];
    }


    void SinglePhotonView::SetDOF1s(std::vector<float> DOF1s)
    {
        DOF1s_ = DOF1s;
    }

    void SinglePhotonView::SetDOF2s(std::vector<float> DOF2s)
    {
        DOF2s_ = DOF2s;
    }

    void SinglePhotonView::SetDOF3s(std::vector<float> DOF3s)
    {
        DOF3s_ = DOF3s;
    }

    void SinglePhotonView::SetRecHits(std::vector<float> recHits)
    {
        recHits_ = recHits;
    }

    void SinglePhotonView::SetDOF1(int DOF1)
    {
        DOF1_ = DOF1;
    }

    void SinglePhotonView::SetDOF2(int DOF2)
    {
        DOF2_ = DOF2;
    }

    void SinglePhotonView::SetDOF3(int DOF3)
    {
        DOF3_ = DOF3;
    }

}

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

