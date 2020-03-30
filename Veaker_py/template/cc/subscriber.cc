/*! 
 * @file {{message_name}}Subscriber.cc
 * This file contains the implementation of the subscriber functions.
 */

#include "{{message_name}}Subscriber.h"

#ifndef __SYNTHESIS__
#include <chrono>
#include <thread>

#include <fastrtps/attributes/ParticipantAttributes.h>
#include <fastrtps/attributes/SubscriberAttributes.h>
#include <fastrtps/Domain.h>
#include <fastrtps/participant/Participant.h>
#include <fastrtps/subscriber/Subscriber.h>
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
{{message_name}}Subscriber::{{message_name}}Subscriber(void) {
    mp_participant = nullptr;
    mp_subscriber = nullptr;

    // Create RTPSParticipant
    ParticipantAttributes PParam_sub;
    //MUST BE THE SAME AS IN THE PUBLISHER
    PParam_sub.rtps.builtin.domainId = 0;
    PParam_sub.rtps.builtin.leaseDuration = c_TimeInfinite;
    //You can put the name you want
    PParam_sub.rtps.setName("Participant_subscriber");

    mp_participant = Domain::createParticipant(PParam_sub);
    if(mp_participant == nullptr)
        exit(1);

    // Register the type
    Domain::registerType(mp_participant, static_cast<TopicDataType*>(&myType));

    // Create Subscriber
    SubscriberAttributes Rparam;
    Rparam.topic.historyQos.kind = KEEP_ALL_HISTORY_QOS;
    Rparam.topic.historyQos.depth = 100;
    Rparam.topic.topicKind = NO_KEY;
    Rparam.topic.topicDataType = myType.getName();
    Rparam.topic.topicName = "/alchemist/user/{{message_name}}";
    Rparam.qos.m_reliability.kind = RELIABLE_RELIABILITY_QOS;

    mp_subscriber = Domain::createSubscriber(mp_participant, Rparam, static_cast<SubscriberListener*>(&m_listener));
    if(mp_subscriber == nullptr)
        exit(1);
}

{{message_name}}Subscriber::~{{message_name}}Subscriber(void) {
    Domain::removeParticipant(mp_participant);
}

void
{{message_name}}Subscriber::SubListener::onSubscriptionMatched(Subscriber* sub, MatchingInfo& info) {
    if (info.status == MATCHED_MATCHING) {
        n_matched++;
    } else {
        n_matched--;
    }
}

void
{{message_name}}Subscriber::SubListener::onNewDataMessage(Subscriber* sub) {
    {{message_name}} st;

    if(sub->takeNextData(&st, &m_info)) {
        if(m_info.sampleKind == ALIVE) {
            std::lock_guard<std::mutex> lock(mtx);
            buffer.push(st);
        }
    }
}
#endif // __SYNTHESIS__

{{message_name}}
{{message_name}}Subscriber::subscribe(void) {
#ifndef __SYNTHESIS__
    while (true) {
        {
            std::lock_guard<std::mutex> lock(m_listener.mtx);
            if (!m_listener.buffer.empty()) {
                {{message_name}} buf = m_listener.buffer.front();
                m_listener.buffer.pop();
                return buf;
            }
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
#else
    {{message_name}} msg;
    MessagePacket packet;
{{subscribe_method}}
    return msg;
#endif
}
