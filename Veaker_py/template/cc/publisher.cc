/*! 
 * @file {{message_name}}Publisher.cc
 * This file contains the implementation of the publisher functions.
 */

#include "{{message_name}}Publisher.h"

#ifndef __SYNTHESIS__
#include <chrono>
#include <thread>

#include <fastrtps/attributes/ParticipantAttributes.h>
#include <fastrtps/attributes/PublisherAttributes.h>
#include <fastrtps/Domain.h>
#include <fastrtps/participant/Participant.h>
#include <fastrtps/publisher/Publisher.h>
#include <fastrtps/utils/eClock.h>

using namespace eprosima::fastrtps;
using namespace eprosima::fastrtps::rtps;
#endif // __SYNTHESIS__

namespace {
    typedef union {
        uint64_t   ul;
        uint32_t   ui[2];
        uint16_t   us[4];
        uint8_t    uc[8];
        int64_t    sl;
        int32_t    si[2];
        int16_t    ss[4];
        int8_t     sc[8];
    } MessagePacket;
} // namespace 

#ifndef __SYNTHESIS__
{{message_name}}Publisher::{{message_name}}Publisher(uint32_t dst) {
    mp_participant = nullptr;
    mp_publisher = nullptr;

    // Create RTPSParticipant
    ParticipantAttributes PParam_pub;
    PParam_pub.rtps.builtin.domainId = 0;
    PParam_pub.rtps.builtin.leaseDuration = c_TimeInfinite;
    PParam_pub.rtps.setName("Participant_publisher");

    mp_participant = Domain::createParticipant(PParam_pub);
    if(mp_participant == nullptr)
        exit(1);

    // Register the type
    Domain::registerType(
        mp_participant,
        static_cast<TopicDataType*>(&myType)
    );

    // Create Publisher
    PublisherAttributes Wparam;
    Wparam.topic.historyQos.kind = KEEP_ALL_HISTORY_QOS;
    Wparam.topic.historyQos.depth = 100;
    Wparam.topic.topicKind = NO_KEY;
    // This type MUST be registered
    Wparam.topic.topicDataType = myType.getName();
    Wparam.topic.topicName = "/alchemist/user/{{message_name}}";
    Wparam.qos.m_reliability.kind = RELIABLE_RELIABILITY_QOS;
    Wparam.qos.m_publishMode.kind = ASYNCHRONOUS_PUBLISH_MODE;
    Wparam.times.heartbeatPeriod.seconds = 0;
    Wparam.times.heartbeatPeriod.fraction = 10 * 1000;

    m_listener.n_destination = dst;
    mp_publisher = Domain::createPublisher(
        mp_participant, Wparam,
        static_cast<PublisherListener*>(&m_listener)
    );

    if(mp_publisher == nullptr)
        exit(1);
}

{{message_name}}Publisher::~{{message_name}}Publisher() {
    Domain::removeParticipant(mp_participant);
}

void
{{message_name}}Publisher::PubListener::onPublicationMatched(Publisher* pub, MatchingInfo& info) {
    if (info.status == MATCHED_MATCHING) {
        n_matched++;
    } else {
        n_matched--;
    }

    if (!publishable && n_matched >= n_destination) {
        publishable = true;
    }
}
#endif // __SYNTHESIS__

void
{{message_name}}Publisher::publish({{message_name}} &msg) {
#ifdef __SYNTHESIS__ // FPGA
    MessagePacket packet;
{{publish_method}}
#else                // C simulation
    while(!m_listener.publishable) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    mp_publisher->write(&msg);
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
#endif
}
